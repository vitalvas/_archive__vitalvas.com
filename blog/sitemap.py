from datetime import datetime

from django.contrib.sitemaps import Sitemap as DjSitemap
from django.core.urlresolvers import reverse

from blog.models import Tag, Article, Page

class Sitemap(DjSitemap):
	changefreq = 'weekly'
	priority = 0.5

	def items(self):
		return Article.objects.filter(publish=True).filter(published__lt=datetime.now())

	def lastmod(self, obj):
		return obj.updated

class Sitemap_tag(DjSitemap):
	changefreq = 'weekly'
	priority = 0.7

	def items(self):
		return Tag.objects.all()

class Main(DjSitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return [ 'home', 'blog', 'blog_archives' ]

	def location(self, item):
		return reverse(item)

class SmPage(DjSitemap):
	changefreq = 'weekly'
	priority = 0.4

	def items(self):
		return Page.objects.filter(state=True)

	def lastmod(self, obj):
		return obj.updated


sitemaps = {
	'main': Main,
	'blog': Sitemap,
	'tag': Sitemap_tag,
	'pages': SmPage,
}

