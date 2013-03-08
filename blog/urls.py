from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'blog.views.index'),
    (r'^blog/$', 'blog.views.blog_list'),
    (r'^blog/([0-9]{4})/([0-9]{2})/([0-9]{2})/([a-zA-Z0-9-]+)+/$', 'blog.views.blog_show'),
    (r'^blog/tags/$', 'blog.views.show_category'),
    (r'^blog/tags/([a-zA-Z0-9]+)/', 'blog.views.show_tag'),
    (r'^links/$', 'blog.views.links'),
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
