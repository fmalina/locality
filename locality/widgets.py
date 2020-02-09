from django import forms
from django.contrib.gis import geos


class PointWidget(forms.MultiWidget):
    """Point widget for Django forms with two hidden inputs for
    latitude and longitude to be used with a JS map
    """
    def __init__(self, widget=None, attrs=None):
        if not widget:
            widget = forms.HiddenInput
        widgets = (widget(attrs=attrs), widget(attrs=attrs))
        super(PointWidget, self).__init__(widgets, attrs)

    @staticmethod
    def to_point(value):
        if isinstance(value, str):
            value = geos.fromstr(value)
        return ["%.6f" % value.x, "%.6f" % value.y]

    def decompress(self, value):
        if value:
            return self.to_point(value)
        return [0, 0]

    def value_from_datadict(self, data, files, name):
        lat, lon = [widget.value_from_datadict(data, files, '%s_%s' % (name, i))
                    for i, widget in enumerate(self.widgets)]
        if not lat or not lon:
            return None
        location = geos.Point(float(lat), float(lon))
        return str(location)
