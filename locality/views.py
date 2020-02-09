from geonames import models as geo_models
from django.shortcuts import render, get_object_or_404
from locality.utils import reject_outliers


def get_context(o, label):
    locs = o.locality_set.all()
    lats = locs.order_by('latitude').values_list('latitude', flat=True)
    lons = locs.order_by('longitude').values_list('longitude', flat=True)
    lats = list(lats)
    print(lats)
    lons = list(lons)
    print(lons)
    d = dict(
        o=o,
        min_lat=lats[0],
        max_lat=lats[-1],
        min_lon=lons[0],
        max_lon=lons[-1],
        metropolis=locs.order_by('population').last()
    )
    d[label] = o
    return d


def world(request):
    countries = geo_models.Country.objects.all()
    return render(request, 'locality/world.html', {'countries': countries})


def country(request, country_code):
    c = get_object_or_404(geo_models.Country, code=country_code)
    context = get_context(c, 'country')
    return render(request, 'locality/country.html', context)


def aa1(request, country_code, aa1_code):
    aa1 = geo_models.Admin1Code.objects.filter(country__code=country_code).filter(code=aa1_code).first()
    return render(request, 'locality/aa1.html', {'aa1': aa1})


def aa2(request, country_code, aa1_code, aa2_code):
    aa2 = geo_models.Admin2Code.objects.filter(country__code=country_code).filter(code=aa2_code).first()
    context = get_context(aa2, 'aa2')
    return render(request, 'locality/aa2.html', context)


def loc(request, geonameid, slug):
    loc = get_object_or_404(geo_models.Locality, geonameid=geonameid)
    return render(request, 'locality/loc.html', {'loc': loc})
