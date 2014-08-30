
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from bookshare.views import (how_it_works)
from bookshare.apps.core import urls
from bookshare.apps.console import urls as console_urls
from bookshare.apps.books.views import BookDetailView, BookSearchView, rent_request

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'bookshare.views.index', name="index"),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^books/', include('bookshare.apps.books.urls', namespace="books")),
   url(r'^how-it-works$', how_it_works, name="how-it-works"),
   url(r'^console', include(console_urls.urlpatterns, namespace="console"))
)

if settings.DEBUG:
   urlpatterns += patterns('',
      url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}), 
   )

