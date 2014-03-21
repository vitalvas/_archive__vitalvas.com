import urllib
from datetime import datetime
from django.core.management.base import BaseCommand
from blog.settings import ping_sitemap, sitemap_url
from blog.models import Page, Article


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		today = datetime.today()
		arr = [
			Page.objects.filter(state=True).filter(updated__year=today.year, updated__month=today.month, updated__day=today.day).count(),
			Article.objects.filter(publish=True).filter(updated__year=today.year, updated__month=today.month, updated__day=today.day).count()
		]
		if any(arr):
			for uurl in ping_sitemap:
				for k in uurl[1]:
					if '%s' in uurl[1][k]:
						uurl[1][k] = sitemap_url
				params = urllib.urlencode(uurl[1])
				f = urllib.urlopen("%s?%s" % (uurl[0],params))
				f.read()
				print uurl[0], '-->', f.code