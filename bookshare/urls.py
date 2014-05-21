
from django.conf.urls import patterns, include, url
from django.contrib import admin

from bookshare.views import (MyPageView, MyPageViewModify, MyRentRequestListView, MyRentListView,
                             MyDonateListView, SignInView, SignUpView, how_it_works)
from bookshare.apps.core import urls
from bookshare.apps.console import urls as console_urls
from bookshare.apps.books.views import BookDetailView, BookSearchView, rent_request

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'bookshare.views.index', name="index"),
   url(r'^signin/$', SignInView.as_view(), name="signin"),
   url(r'^signup/$', SignUpView.as_view(), name="signup"),
   url(r'^signout/$', 'bookshare.views.signout'),
   url(r'^me/$', MyPageView.as_view(), name="mypage"),
   url(r'^me/modify$', MyPageViewModify.as_view(), name="mypage-modify"),
   url(r'^my/rent\-requests/$', MyRentRequestListView.as_view(), name='my-rent-requests'),
   url(r'^my/rents/$', MyRentListView.as_view()),
   url(r'^my/donates/$', MyDonateListView.as_view()),

   url(r'^admin/', include(admin.site.urls)),
   url(r'^test/', include(urls.urlpatterns, namespace="core")),
   url(r'^books/', include('bookshare.apps.books.urls', namespace="books")),
   url(r'^how-it-works$', how_it_works, name="how-it-works"),
   url(r'^console', include(console_urls.urlpatterns, namespace="console")),
)

