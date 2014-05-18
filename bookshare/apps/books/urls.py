from django.conf.urls import patterns, include, url
from bookshare.apps.books.views import BookSearchView, BookRentView, BookDetailView
import views

urlpatterns = patterns('',
   url(r'^(?P<pk>[0-9]+)/$', BookDetailView.as_view(), name='book-detail'),
   url(r'^(?P<pk>[0-9]+)/rent/$', BookRentView.as_view(), name='rent-request'),
   url(r'^search/$', BookSearchView.as_view()),
)
