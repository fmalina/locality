from math import radians, degrees, sqrt, sin, cos, atan2

EARTH_R = 3959  # miles / 6372.8 km


def distance(p1, p2):
    """Return a distance between two points on the globe"""
    lat1, lon1 = radians(p1.x), radians(p1.y)
    lat2, lon2 = radians(p2.x), radians(p2.y)
    dlon = lon1 - lon2
    y = sqrt(
        (cos(lat2) * sin(dlon)) ** 2 +
        (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
    )
    x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
    c = atan2(y, x)
    return EARTH_R * c


def bearing(p1, p2):
    """Return a bearing from A to B given two points."""
    lat1, lon1 = p1.x, p1.y
    lat2, lon2 = p2.x, p2.y

    angle = atan2(lat1 - lat2, lon1 - lon2)
    a = int(round(degrees(angle)))
    m = 90/4 + 1  # margin tolerance
    for k, v in zip("south east north SW SE NE NW".split(),
                    (-90, 0, 90, -135, -45, 45, 135)):
        if v-m < a < v+m:
            return k
    return "West"
