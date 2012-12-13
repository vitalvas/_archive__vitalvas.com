#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2, urllib2, json, re, os
from datetime import datetime
from lib import markdown2 as markdown
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import memcache
from keys import instagram_token

if os.getcwd() == "/Users/vitalvas/Yandex.Disk/GoogleAppEngine/blogek":
	use_memcache=False
	is_debug=True
else:
	use_memcache=True
	is_debug=False

class Post(db.Model):
	name = db.StringProperty()
	title = db.StringProperty(indexed=False)
	date = db.DateProperty(auto_now_add=True)
	sort_date = db.DateTimeProperty(auto_now_add=True)
	publish = db.BooleanProperty(default=True)
	publish_rss = db.BooleanProperty(default=True)
	data = db.TextProperty(indexed=False)
	categories = db.StringProperty(indexed=False)


class Links(db.Model):
	link = db.StringProperty(indexed=False)
	pre_title = db.StringProperty(indexed=False)
	title = db.StringProperty(indexed=False)
	post_title = db.StringProperty(indexed=False)
	date = db.DateTimeProperty(auto_now_add=True)
	publish = db.BooleanProperty(default=True)


class BlogOutputWorker():
	def __init__(self, query):
		self.domain = 'http://www.vitalvas.com'
		self.data = query.data
		self.name = query.name
		self.date = query.date
		self.title = query.title
		self.categories = query.categories
		self.publish = query.publish
		self.sort_date = query.sort_date
		self.__youtube()
		self.__markdown()
		self.__split()
		self.__generate_url()
		self.__public_date()
	def __split(self):
		spt = self.data.replace("<!-- more -->", "<!--more-->")
		spt = spt.split("<!--more-->")
		if len(spt)>1:
			self.read_more = True
			self.data_full = self.data
			self.data = spt[0]
		else:
			self.read_more = False
			self.data_full = self.data
	def __markdown(self):
		self.data = markdown.markdown(self.data, extras=["cuddled-lists","wiki-tables","nofollow"])
	def __generate_url(self):
		self.url = "/blog/%s/%s/" % (datetime.strftime(self.date, "%Y/%m/%d"), self.name)
	def __public_date(self):
		self.public_date = datetime.strftime(self.date, "%d-%m-%Y")
	def __youtube(self):
		regex = re.compile('{% youtube ([A-Za-z0-9-_]{11}) %}')
		data = self.data
		match = regex.findall(data)
		for video_id in match:
			render_frame = '<div class="embed-video-container"><iframe src="http://www.youtube.com/embed/%s?autohide=1&egm=0&hd=1&iv_load_policy=3&modestbranding=1&rel=0&showinfo=0&showsearch=0&theme=light" frameborder="0" allowfullscreen></iframe></div>' % video_id
			tag = "{% youtube video_id %}"
			tag = tag.replace("video_id", video_id)
			self.data = self.data.replace(tag,render_frame)


class MainHandler(webapp2.RequestHandler):
    def get(self):
		if users.is_current_user_admin():
			data_out = template.render('templates/main.html',{'type':'index',
				'login_url':users.create_login_url(self.request.uri),
				'logout_url':users.create_logout_url(self.request.uri),
				'is_admin':True
			})
		else:
			try:
				if use_memcache is False: raise Exception("Cache disabled")
				if use_memcache: data_out = memcache.get("main")
				if not data_out: raise Exception("Data not in cache")
			except:
				data_out = template.render('templates/main.html',{'type':'index',
					'login_url':users.create_login_url(self.request.uri),
					'logout_url':users.create_logout_url(self.request.uri),
					'is_admin':users.is_current_user_admin()
				})
				if use_memcache: memcache.get("main", data_out, 3600)
		self.response.write(data_out)


class ShowBlog(webapp2.RequestHandler):
	def get(self):
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data = memcache.get("blog")
			if not data: raise Exception("Data not in cache")
		except:
			query = db.GqlQuery("SELECT * FROM Post WHERE publish=True ORDER BY sort_date DESC").fetch(7)
			res = []
			for line in query:
				res.append(BlogOutputWorker(line))
			data = template.render('templates/bloglist.html',{'type':'blog','posts':res})
			if use_memcache: memcache.add("blog", data, 3600)
		finally:
			self.response.write(data)

class ShowBlogRss(webapp2.RequestHandler):
	def get(self):
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data_out = memcache.get("blog-rss")
			if not data_out: raise Exception("Data not in cache")
		except:
			query = db.GqlQuery("SELECT * from Post WHERE publish=True AND publish_rss=True ORDER BY sort_date DESC").fetch(10)
			resp = []
			for line in query:
				resp.append(BlogOutputWorker(line))
			data_out = template.render('templates/atom.xml',{'posts':resp})
			if use_memcache: memcache.add("blog-rss", data_out, 3600)
		finally:
			self.response.write(data_out)
			self.response.headers.add_header("Content-type", 'text/xml')
		

class NewBlogPost(webapp2.RequestHandler):
	def get(self):
		self.response.write(template.render('templates/newpage.html',{'type':'blog','page':'blog'}))
	def post(self):
		post = Post()
		post.data = self.request.get('content')
		post.name = self.request.get('name')
		post.title = self.request.get('title')
		post.categories = self.request.get('categories')
		post.put()
		if use_memcache: memcache.delete("blog")
		self.redirect('/blog/')
		

class ShowBlogPost(webapp2.RequestHandler):
	def get(self,year,month,day,name):
		date = "%s-%s-%s" % (year,month,day)
		cache_key = "blog-%s-%s" % (date, name)
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data_out = memcache.get(cache_key)
			if not data_out: raise Exception("Data not in cache")
		except:
			res = db.GqlQuery("SELECT * FROM Post WHERE name=:1 AND date=DATE(:2)", name, date).get()
			if not res:
				self.error(404)
				data_out = template.render('templates/error.html',{'error':'404','error_msg':'Not found'})
				if use_memcache: memcache.add(cache_key, data_out, 30)
			else:
				if res.publish is True or users.is_current_user_admin():
					res = BlogOutputWorker(res)
					data_out = template.render('templates/blogpost.html',{'post':res,"name":name, 'type':'blog'})
					if use_memcache: memcache.add(cache_key, data_out, 3600)
				else:
					self.error(404)
					data_out = template.render('templates/error.html',{'error':'404','error_msg':'Not found'})
					if use_memcache: memcache.add(cache_key, data_out, 30)
		finally:
			self.response.write(data_out)


class ShowSitemap(webapp2.RequestHandler):
	def get(self):
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data_out = memcache.get("sitemap")
			if not data_out: raise Exception("Data not in cache")
		except:
			req = db.GqlQuery("SELECT * FROM Post WHERE publish=True ORDER BY sort_date DESC")
			resp = []
			for line in req:
				resp.append(BlogOutputWorker(line))
			data_out = template.render("templates/sitemap.xml",{'post':resp})
			if use_memcache: memcache.add("sitemap", data_out, 3600)
		finally:
			self.response.out.write(data_out)
			self.response.headers.add_header("Content-type", 'text/xml')


class ShowCreative(webapp2.RequestHandler):
	def get(self):
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data_out = memcache.get("creative")
			if not data_out: raise Exception("Data not in cache")
		except:
			inst_cache = memcache.get("instagram-photos")
			if not inst_cache:
				data = urllib2.urlopen("https://api.instagram.com/v1/users/203723320/media/recent/?count=10&access_token=%s" % instagram_token )
				if data:
					inst_json_data = json.load(data)
					inst_cache = []
					for js in inst_json_data['data']: 
						inst_cache.append(js['images'])
					memcache.add("instagram-photos", inst_cache, 10800) # 3h
			data_out = template.render('templates/creative.html',{'type':'creative','inst_photos':inst_cache})
			if use_memcache: memcache.add("creative", data_out, 3600)
		finally:
			self.response.write(data_out)


class NewLink(webapp2.RequestHandler):
	def get(self):
		link_data = {}
		if self.request.get("url"):
			link_data['url'] = self.request.get("url")
			if self.request.get("descr"):
				link_data["title"] = self.request.get("descr")
			else:
				data = urllib2.urlopen(self.request.get("url")).read()
				if data:
					link_data["title"] = data.split('<title>')[1].split('</title>')[0].strip()
		self.response.write(template.render('templates/newlink.html',link_data))
	def post(self):
		post = Links()
		post.link = self.request.get('url')
		post.title = self.request.get('name')
		post.pre_title = self.request.get('pre_name')
		post.post_title = self.request.get('post_name')
		if self.request.get('publish') == 'True':
			post.publish = True
		else:
			post.publish = False
		post.put()
		if use_memcache: memcache.delete("links")
		if self.request.get('topframe'):
			self.response.write("Published :)<script type='text/javascript'>window.close();</script>")
		else:
			self.redirect('/links/')


class ShowLinks(webapp2.RequestHandler):
	def get(self):
		try:
			if use_memcache is False: raise Exception("Cache disabled")
			if use_memcache: data_out = memcache.get("links")
			if not data_out: raise Exception("Data not in cache")
		except:
			query = db.GqlQuery("SELECT * FROM Links WHERE publish=True ORDER BY date DESC").fetch(50)
			data_out = template.render("templates/links.html",{'type':'links','links':query})
			if use_memcache: memcache.add("links", data_out, 3600)
		finally:
			self.response.write(data_out)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/blog/', ShowBlog),
	('/blog/new_post', NewBlogPost),
	('/blog/([0-9]{4})/([0-9]{2})/([0-9]{2})/([a-zA-Z0-9-]+)+/', ShowBlogPost),
	('/blog/atom.xml', ShowBlogRss),
	('/sitemap.xml', ShowSitemap),
	('/creative/', ShowCreative),
	('/links/', ShowLinks),
	('/links/new_link', NewLink)
], debug=is_debug)
