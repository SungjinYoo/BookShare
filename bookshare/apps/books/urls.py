from django.conf.urls import patterns, include, url
from bookshare.apps.books.views import BookSearchView, BookDetailView
import views

urlpatterns = patterns('',
   url(r'^$', BookSearchView.as_view(), name="book-list"),
   url(r'^(?P<pk>[0-9]+)/$', BookDetailView.as_view(), name='book-detail'),
   url(r'^rent\-request/$', views.rent_request, name='book-rent-request'),
   url(r'^cancel\-rent\-request/$', views.cancel_rent_request, name='book-cancel-rent-request'),
   url(r'^return\-request/$', views.return_request, name='book-return-request'),
   url(r'^cancel\-return\-request/$', views.cancel_return_request, name='book-cancel-return-request'),
)
