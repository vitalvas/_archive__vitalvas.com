from django.template import Library

register = Library()

@register.filter()
def cut_preview(value):
	value = value.split('<!--more-->')[0]
	value = value.split('<!-- more -->')[0]
	return value


