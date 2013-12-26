#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytils
from django.db import models
from django.contrib import admin
from markdown2 import markdown
from datetime import datetime
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
	publish = models.BooleanField(default=True, db_index=True)
	data = models.TextField()
	html_compile = models.TextField(editable=False)
	tags = models.ManyToManyField(Tag)
	pinged = models.BooleanField(default=False)
	updated = models.DateTimeField()
	def __unicode__(self):
		return self.title
	def save(self, *args, **kwargs):
		self.html_compile = markdown(self.data)
		self.updated = datetime.now()
		if not self.slug:
			self.slug = pytils.translit.slugify(self.title)
		super(Article, self).save(*args, **kwargs)
	class Meta:
		ordering=('-published',)


