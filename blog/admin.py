from django.contrib import admin
from blog.models import *

admin.site.register(Article,
        list_display = ('slug', 'title', 'published', 'publish', 'pinged'),
        date_hierarchy = 'published',
        list_filter = ('publish', 'tags'),
        filter_horizontal = ('tags',),
        search_fields = ('slug', 'title')
)

admin.site.register(Tag, list_display = ('slug', 'title',), search_fields=('title',))

