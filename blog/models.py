#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytils
from django.db import models
from django.contrib import admin
from markdown2 import markdown
from django.forms import TextInput, Textarea


class Tag(models.Model):
	slug = models.SlugField(unique=True, blank=True)
	title = models.CharField(max_length=80)
	def __unicode__(self):
		return self.title
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = pytils.translit.slugify(self.title)
		super(Tag, self).save(*args, **kwargs)
	class Meta:
		ordering = ('title',)


class Article(models.Model):
	slug = models.SlugField(unique=True, blank=True)
	title = models.CharField(max_length=100)
	published = models.DateTimeField(blank=True, null=True, db_index=True)
	publish = models.BooleanField(default=True)
	data = models.TextField()
	html_compile = models.TextField(editable=False)
	tags = models.ManyToManyField(Tag)
	pinged = models.BooleanField(default=False)
	def __unicode__(self):
		return self.title
	def save(self, *args, **kwargs):
		self.html_compile = markdown(self.data)
		if not self.slug:
			self.slug = pytils.translit.slugify(self.title)
		super(Article, self).save(*args, **kwargs)
	class Meta:
		ordering=('-published',)


class Link(models.Model):
	link = models.CharField(max_length=200)
	pre_title = models.TextField(blank=True, null=True)
	title = models.TextField()
	post_title = models.TextField(blank=True, null=True)
	published = models.DateTimeField(db_index=True)
	publish = models.BooleanField(default=True)
	pinged = models.BooleanField(default=False)
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ('-published','id')


class AdminLink(admin.ModelAdmin):
	list_display = ('id', 'pre_title', 'title', 'post_title', 'published', 'publish')
	date_hierarchy = 'published'
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':55}) },
		models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}
	}
admin.site.register(Link, AdminLink)




admin.site.register(Article, list_display = ('slug', 'title', 'published', 'publish', 'pinged'),
	date_hierarchy = 'published', list_filter = ('publish', 'tags'),
	filter_horizontal = ('tags',), search_fields = ('slug', 'title'))



admin.site.register(Tag, list_display = ('slug', 'title',), search_fields=('title',))



