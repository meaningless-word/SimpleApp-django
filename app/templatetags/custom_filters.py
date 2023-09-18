from django import template

register = template.Library()


CURRENCY_SYMBOLS = {
    'rub': '₽',
    'usd': '$',
}

@register.filter()
def currency(value, code='rub'):
    """
    :param value: значение, к которому нужно применить фильтр
    :param code: код валюты
    :return:
    """
    postfix = CURRENCY_SYMBOLS[code]
    return f'{value} {postfix}'