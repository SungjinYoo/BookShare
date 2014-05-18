from django.conf.urls import patterns, include, url
from bookshare.apps.books.views import BookSearchView, BookDetailView
import views

urlpatterns = patterns('',
   url(r'^(?P<pk>[0-9]+)/$', BookDetailView.as_view(), name='book-detail'),
   url(r'^search/$', BookSearchView.as_view()),
   url(r'^rent\-request$', views.rent_request, name='book-rent-request'),
)
