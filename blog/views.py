#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from django.shortcuts import render_to_response
from django.http import Http404
from blog.models import *
from datetime import datetime

CONF = dict(domain='http://new.vitalvas.com')

index = lambda self: render_to_response('main.html', dict(type='index'))

links = lambda self: render_to_response('links.html', dict(type='links', links=Link.objects.filter(publish=True)[:50]))

def blog_list(self):
	items_orig = Article.objects.filter(publish=True).filter(published__lt=datetime.now()).order_by('-published')[:10]
	items = []
	for it in items_orig:
		it.url = '/blog/%s/%s/' % ( str(it.published).replace('-','/').split(' ')[0], it.slug )
		it.html_compile = it.html_compile.replace('<!-- more -->', '<!--more-->')
		it.html_compile = it.html_compile.split("<!--more-->")[0]
		items.append(it)
	return render_to_response('blog.html', dict(type='blog', act='list', posts=items, conf=CONF))

def blog_show(self, year, month, day, name):
#	try:
		item = Article.objects.get(slug=name, published__year=year, published__month=month, published__day=day)
		item.url = '/blog/%s/%s/' % ( "/".join([year, month, day]), name )
		og_img = re.findall('img .*?src="(.*?)"', item.html_compile)
		if og_img:
			item.og_img = og_img[0]
#	except:
#		raise Http404
#	else:
		return render_to_response('blog.html', dict(type='blog', act='post', post=item, conf=CONF))


def show_category(self):
	items = Category.objects.all()
	return render_to_response('blog.html', dict(type='blog', act='category', tags=list(items)))

show_tag = show_category