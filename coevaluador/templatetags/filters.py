from django.template.defaultfilters import register


@register.filter(name='getkey')
def getKey(d:dict, key):
    if key in d:
        return d[key]
    return None