#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random
from markdown2 import markdown
from pytils.translit import slugify
from datetime import datetime

from django.db import models

class Tag(models.Model):
	slug = models.SlugField(unique=True, blank=True)
	title = models.CharField(max_length=80)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Tag, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
		return ('blog_tag', (self.slug,))

	class Meta:
		ordering = ('title',)

class Article(models.Model):
	slug = models.SlugField(blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	token = models.CharField(max_length=20, blank=True, db_index=True)
	title = models.CharField(max_length=100)
	published = models.DateTimeField(blank=True, null=True, db_index=True)
	publish = models.BooleanField(default=True, db_index=True)
	data = models.TextField()
	html_compile = models.TextField(editable=False)
	updated = models.DateTimeField(editable=False, auto_now=True)
	description = models.CharField(max_length=250, blank=True)
	image = models.CharField(max_length=250, blank=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.html_compile =  u'%s' % markdown(self.data,
				['footnotes', 'admonition', 'headerid', 'nl2br', 'tables', 'wikilinks', 'pyshell'])
		self.updated = datetime.now()
		if not self.slug:
			self.slug = slugify(self.title)
		if self.publish and not self.published:
			self.published = datetime.now()
		if not self.token:
			self.token = ''.join([random.choice(string.ascii_letters + string.digits) for x in xrange(20)])
		super(Article, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
		return ('blog_show', (self.published.year, '%02d' % int(self.published.month), '%02d' % int(self.published.day), self.slug))

	class Meta:
		ordering = ('-published',)


class Page(models.Model):
	slug = models.SlugField(blank=True)
	title = models.CharField(max_length=150)
	state = models.BooleanField(default=False)
	data = models.TextField()
	html_compile = models.TextField(editable=False)
	updated = models.DateTimeField(editable=False, auto_now=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.html_compile = u'%s' % markdown(self.data,
				['footnotes', 'admonition', 'headerid', 'nl2br', 'tables', 'wikilinks', 'pyshell'])
		self.updated = datetime.now()
		if not self.slug:
			self.slug = slugify(self.title)
		super(Page, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
		return ('page', (self.slug,))

