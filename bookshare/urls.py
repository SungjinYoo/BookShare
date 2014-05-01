from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = (
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'^', include('bookshare.apps.books.urls', namespace="books")),
    url(r'^core/', include('bookshare.apps.core.urls', namespace="core")),

    url(r'^admin/', include(admin.site.urls)),
)
