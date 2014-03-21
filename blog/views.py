#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyatom import AtomFeed
from datetime import datetime

from django import db
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

from blog.models import Tag, Article, Page
from blog.templatetags.display import cut_preview

handler404 = lambda self: render_to_response('404.html', {'request': self.get_full_path()})

def home(self):
	db.reset_queries()
	ctx = {
		'request': self.get_full_path(),
		'items': Article.objects.filter(publish=True)[:4],
	}
	return render_to_response('base.html', ctx)

def blog(self, tag=False):
	db.reset_queries()
	items = Article.objects.filter(publish=True).filter(published__lt=datetime.now())
	if tag:
		tag = get_object_or_404(Tag, slug=tag)
		items = items.filter(tags=tag)
	ctx = {
		'request': self.get_full_path(),
		'tag': tag,
		'items': items[:7],
	}
	return render_to_response('list.html', ctx)


def blog_show(self, year=0, month=0, day=0, slug='', token=False):
	db.reset_queries()
	if token and not year and not month and not day and not slug:
		item = get_object_or_404(Article, token=token)
		if item.publish:
			return HttpResponsePermanentRedirect(item.get_absolute_url())
	else:
		item = get_object_or_404(Article, published__year=year, published__month=month, published__day=day, slug=slug)
	ctx = {
		'request': self.get_full_path(),
		'item': item,
	}
	return render_to_response('show.html', ctx)

def blog_archive(self):
	db.reset_queries()
	ctx = {
		'request': self.get_full_path(),
		'items': Article.objects.filter(publish=True).filter(published__lt=datetime.now())
	}
	return render_to_response('archive.html', ctx)


def show_page(self, url):
	db.reset_queries()
	ctx = {
		'request': self.get_full_path(),
		'item': get_object_or_404(Page, slug=url, state=True)
	}
	return render_to_response('page.html', ctx)


def feed(self):
	db.reset_queries()
	url = ''.join(['https://' if self.is_secure() else 'http://', self.get_host()])
	feed = AtomFeed(
		title = 'The VitalVas',
		url = url,
		feed_url = ''.join([url, reverse('feed')]),
		author = {
			'name': 'VitalVas',
			'email': 'feed@vitalvas.com'
		},
	)
	for item in Article.objects.filter(publish=True).filter(published__lt=datetime.now())[:5]:
		feed.add(
			title = item.title,
			content = cut_preview(item.html_compile),
			content_type = 'html',
			author = 'VitalVas',
			url = ''.join([url, item.get_absolute_url()]),
			updated = item.updated,
		)
	return HttpResponse(feed.to_string(), content_type='text/xml')

