from math import pi, sin, radians
from django.contrib.gis.geos import LinearRing, Polygon
from django.db import models
from geonames.models import near_places_rough

EARTH_R = 3959


class LocationManager(models.Manager):
    def square_area(self, S, W, N, E):
        # Mercator style "square"
        S, W, N, E = [round(x, 3) for x in (S, W, N, E)]
        SW = S, W
        SE = S, E
        NE = N, E
        NW = N, W
        # corners counterclockwise, 4326: GPS lat lon system
        return Polygon(LinearRing(SW, SE, NE, NW, SW, srid=4326), srid=4326)

    def near_within_square(self, coords, radius=0):
        """Using spatial index, bring up all adverts within radius."""
        earth_r = 3959  # miles = 6371 km
        lat, lon = coords
        circ = sin(radians(90 - lat)) * earth_r * pi * 2  # circumference at latitude of the search
        r = (radius / circ * 360)  # radius converted to degrees
        S, W = lat - r, lon - r
        N, E = lat + r, lon + r
        return self.filter(coords__within=self.square_area(S, W, N, E))

    def area(self, coords, coords2):
        S, W = coords  # south west corner (lower left)
        N, E = coords2  # north east corner
        return self.filter(coords__within=self.square_area(S, W, N, E))

    def near(self, coords, radius=20, typ='', limit=100):
        table = self.model._meta.db_table
        pk = self.model._meta.pk.name
        if typ:
            typ = f'AND typ = "{typ[0]}"'

        bbox = near_places_rough(self.model, coords.x, coords.y, miles=radius, sql=True)

        qs = self.raw(f"""
            SELECT {pk},
            ST_Distance_Sphere(
                coords,
                ST_GeomFromText('POINT({coords.x} {coords.y})', 4326),
                {EARTH_R}
            ) AS distance
            FROM {table}
            WHERE {bbox}
            coords IS NOT NULL {typ}
            HAVING distance < {radius}
            ORDER BY distance
            LIMIT {limit}
        """)
        # """"""
        pks = [o.pk for o in qs]
        distances = {o.pk: round(o.distance, 1) for o in qs}

        qs = self.filter(pk__in=pks)
        only = getattr(self.model, 'only', [])
        if only:
            only = self.model.only + ['urn', 'name', 'postcode']
            qs = qs.only(*only)
        for o in qs:
            setattr(o, 'distance', distances[o.pk])
        if typ or table == 'school':
            qs = sorted(list(qs), key=lambda x: x.distance)
        return qs
