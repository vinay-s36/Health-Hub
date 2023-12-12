# custom_filters.py
from django import template

register = template.Library()


@register.filter(name='truncate_words')
def truncate_words(value, num_words):
    words = value.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return value
