#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, xmlrpclib, pyatom, pysitemap
from datetime import datetime

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.db import connection

from blog.models import *
from blog.settings import ping

CONF = dict(domain='http://www.vitalvas.com', name='VitalVas здесь был')

index = lambda self: render_to_response('main.html', dict(type='index'))

def blog_list(self, tag=False):
	if tag:
		items_orig = Article.objects.filter(tags__slug__exact=tag).filter(publish=True).filter(published__lt=datetime.now())[:10]
	else:
		items_orig = Article.objects.filter(publish=True).filter(published__lt=datetime.now())[:10]
	items = []
	for it in items_orig:
		it.url = '/blog/%s/%s/' % ( str(it.published).replace('-','/').split(' ')[0], it.slug )
		it.html_compile = it.html_compile.replace('<!-- more -->', '<!--more-->')
		it.html_compile = it.html_compile.split("<!--more-->")[0]
		items.append(it)
		if it.pinged is False:
			for ping_link in ping:
				try:
					rpc = xmlrpclib.Server(ping_link)
					rpc.weblogUpdates.ping(CONF['name'], CONF['domain'], ''.join([CONF['domain'], it.url]))
				except:
					pass
			post = Article.objects.get(slug=it.slug, published=it.published)
			post.pinged = True
			post.save()
	return render_to_response('blog.html', dict(type='blog', act='list', posts=items, conf=CONF))

def blog_show(self, year, month, day, name):
	try:
		item = Article.objects.get(slug=name, published__year=year, published__month=month, published__day=day)
		item.url = '/blog/%s/' % "/".join([year, month, day, name])
		og_img = re.findall('img .*?src="(.*?)"', item.html_compile)
		if og_img:
			item.og_img = og_img[0]
	except:
		raise Http404
	else:
		return render_to_response('blog.html', dict(type='blog', act='post', post=item, conf=CONF))

def rss(self):
	items = Article.objects.filter(publish=True).filter(published__lt=datetime.now())[:15]
	feed = pyatom.AtomFeed(
		title=str(CONF['name']).decode('utf-8'),
		feed_url='http://www.vitalvas.com/feed.blog',
		url=CONF['domain'],
		author='Виталий Василенко'.decode('utf-8')
	)
	for item in items:
		feed.add(
			title=item.title,
			content=item.html_compile,
			content_type='html',
			author='VitalVas',
			url='/'.join([CONF['domain'],'blog',str(item.published).replace('-','/').split(' ')[0], item.slug, '']),
			updated=item.updated
		)
	return HttpResponse(feed.to_string(), content_type='text/xml')


def sitemap(self):
	xml = pysitemap.SiteMap(domain=CONF['domain'], timezone='+02:00')
	for i in ['blog/', 'blog/archives/']:
		xml.add(loc="/".join([CONF['domain'], i]), changefreq='daily')
	for item in Article.objects.filter(publish=True):
		xml.add(
			loc="/".join([CONF['domain'], 'blog', str(item.published).replace('-','/').split(' ')[0], item.slug, '']),
			priority=0.75,
			lastmod=item.published,
			changefreq='weekly'
		)
	for item in Tag.objects.all():
		xml.add(
			loc='/'.join([CONF['domain'], 'blog', 'tags', item.slug, '']),
			priority=0.3,
			changefreq='monthly'
		)
	return HttpResponse(xml.to_string(), content_type='text/xml')

