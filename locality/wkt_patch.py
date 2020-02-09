"""Patch for loading geonames localities

Import to your settings like this:

    from locality.wkt_patch import WKTAdapter  # noqa
"""

from django.contrib.gis.db.backends.base.adapter import WKTAdapter


def wkt_translate_monkey(self, table):
    return str(self).translate(table)


WKTAdapter.translate = wkt_translate_monkey
