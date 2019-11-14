from django import template

register = template.Library()


@register.filter
def shorten_text(value):
	return value[:305] + '...' if len(value) >= 305 else value
