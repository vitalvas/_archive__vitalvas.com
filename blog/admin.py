#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from blog.models import Tag, Article, Page

admin.site.register(
	Article,
	list_display = ('slug', 'title', 'published', 'publish', 'token', 'updated'),
	date_hierarchy = 'published',
	filter_horizontal = ('tags',),
	fieldsets = (
		(None, {'fields': ('slug' ,'title', 'token')}),
		(None, {'fields': ('data', 'tags')}),
		(None, {'fields': ('published', 'publish')}),
		(None, {'fields': ('description', 'image')}),
	)
)

admin.site.register(
	Tag,
	list_display = ('slug', 'title',),
	search_fields = ('title',),
)

admin.site.register(
	Page,
	list_display = ('slug', 'title', 'state', 'updated'),
)
