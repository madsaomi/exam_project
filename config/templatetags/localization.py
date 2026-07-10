from django import template

register = template.Library()


@register.simple_tag
def localized(obj, field='name', lang='ru'):
    if obj is None:
        return ''
    method = getattr(obj, '_t', None)
    if method:
        return method(field, lang)
    return getattr(obj, field, '')


@register.filter
def trans(obj, lang):
    if not obj or not lang:
        return obj
    return obj._t('name', lang) if hasattr(obj, '_t') else str(obj)
