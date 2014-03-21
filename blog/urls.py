from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from blog.sitemap import sitemaps

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'blog.views.home', name='home'),
	url(r'^page/([a-zA-Z0-9-]+)/$', 'blog.views.show_page', name='page'),
	url(r'^blog/$', 'blog.views.blog', name='blog'),
	url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]{2})/([a-zA-Z0-9-]+)/$', 'blog.views.blog_show', name='blog_show'),
	url(r'^blog/token/(?P<token>[a-zA-Z0-9]{20})/$', 'blog.views.blog_show', name='blog_show_token'),
	url(r'^blog/tag/([a-zA-Z0-9-]+)/$', 'blog.views.blog', name='blog_tag'),
	url(r'^blog/archives/$', 'blog.views.blog_archive', name='blog_archives'),
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	url(r'^feed/$', 'blog.views.feed', name='feed'),
	url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'blog.views.handler404'

