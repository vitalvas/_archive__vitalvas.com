#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, xmlrpclib
from django.shortcuts import render_to_response
from django.http import Http404
from django.db import connection
from blog.models import *
from datetime import datetime
from blog.settings import ping

CONF = dict(domain='http://www.vitalvas.com', name='VitalVas здесь был')

index = lambda self: render_to_response('main.html', dict(type='index'))

links = lambda self: render_to_response('links.html', dict(type='links', links=Link.objects.filter(publish=True)[:50]))

sitemap = lambda self: render_to_response('sitemap.xml', dict(post=Article.objects.filter(publish=True)), mimetype="application/xml")

def blog_list(self):
	items_orig = Article.objects.filter(publish=True).filter(published__lt=datetime.now()).order_by('-published')[:10]
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


def show_tag(self, tag=False):
	items = Tag.objects.all()
	return render_to_response('blog.html', dict(type='blog', act='tags', tags=items))

def rss(self):
	cursor = connection.cursor()
	cursor.execute("""
		SELECT * FROM 
		(SELECT 
			concat('http://www.vitalvas.com/blog/',to_char(DATE(published), 'YYYY/MM/DD'),'/',slug, '/') AS link,
			title,
			'post' AS type,
			published,
			data AS content
			FROM blog_article WHERE publish='t' AND published<NOW()) a 
		UNION ALL SELECT * FROM 
		(SELECT 
			link,
			concat(pre_title,' ',title,' ',post_title) AS title,
			'link' AS type,
			published,
			'' AS content
			FROM blog_link WHERE publish='t' AND published<NOW()) b 
		ORDER BY published DESC LIMIT 15
		""")
	rows = cursor.fetchall()
	return render_to_response('rss.xml', dict(items=rows, now=datetime.now()), mimetype="application/rss+xml")
