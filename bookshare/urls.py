from django.conf.urls import patterns, include, url
from django.contrib import admin

from bookshare.views import MyPageView, SignInView, SignUpView
from bookshare.apps.core import urls
from bookshare.apps.books.views import BookDetailView, rent_request

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'bookshare.views.index'),
   url(r'^signin/$', SignInView.as_view()),
   url(r'^signup/$', SignUpView.as_view()),
   url(r'^signout/$', 'bookshare.views.signout'),
   url(r'^me/$', MyPageView.as_view()),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^test/', include(urls.urlpatterns, namespace="core")),
   url(r'^books/(?P<pk>[0-9]+)$', BookDetailView.as_view(), name='book-detail'),
   url(r'^books/(?P<pk>[0-9]+)/rent\-request$', rent_request, name='book-rent-request'),
)

