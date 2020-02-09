import operator
from functools import reduce

from django.db.models import Q


class TownSearch:
    """
    Handle town name variants such as:

    Weston Super Mare / Weston-Super-Mare
    Shepherd's Bush / Shepherds Bush
    Burton upon Trent / Burton-on-Trent / Burton
    St Helens / St. Helens / Saint Helens

    So that when searching for one, results match other variants too.
    """
    VARIANTS = (
        (' upon ', ' on ', '-on-', '-upon-'),
        ('st ', 'st. ', 'saint '),
        ("'s ", 's '),
        ('-', ' '),
    )

    def variants(self, q):
        q = q.lower().title()
        for var in self.VARIANTS:
            for v in var:
                if v in q:
                    return [q.replace(v, diff) for diff in var]
        return [q]

    def find(self, model, q, exact_match=False, prefetch=None, country_id='gb'):
        match = 'name'
        if not exact_match:
            match += '__istartswith'

        q_list = [(match, i) for i in self.variants(q)]
        q_list = [Q(x) for x in q_list]
        qs = model.objects.filter(reduce(operator.or_, q_list))
        if country_id:
            qs = qs.filter(country_id=country_id)
        if prefetch:
            qs = qs.prefetch_related(prefetch)
        return qs.order_by('-population')


def shorten_street(x):
    """Conventionally shorten various street names."""

    d = {
        ' Street': ' St',
        ' Road': ' Rd',
        ' Drive': ' Dr',
        ' Lane': ' Ln',
        ' Park': ' Pk',
        ' Close': ' Cl',
        ' Avenue': ' Ave',
    }
    for k, v in d.items():
        x = x.replace(k, v)\
             .replace(k.lower(), v)
    return x.strip()
