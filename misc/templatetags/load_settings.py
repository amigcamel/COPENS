# -*- coding: utf-8 -*-


from django import template
from django.conf import settings

register = template.Library()


# settings value
@register.simple_tag
def settings_value(name, *args):
    res = getattr(settings, name, "")

    it = iter(args)
    while True:
        try:
            k = it.next()
            res = res[k]
        except StopIteration:
            return res
        except Exception:
            raise
