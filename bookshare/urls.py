from django.conf.urls import patterns, include, url
from django.contrib import admin

from bookshare.views import MyPageView, MyRentRequestListView, MyRentListView, MyDonateListView, SignInView, SignUpView
from bookshare.apps.core import urls
from bookshare.apps.books.views import BookDetailView, BookSearchView, BookRentView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'bookshare.views.index'),
                       url(r'^signin/$', SignInView.as_view()),
                       url(r'^signup/$', SignUpView.as_view()),
                       url(r'^signout/$', 'bookshare.views.signout'),
                       url(r'^me/$', MyPageView.as_view()),
                       url(r'^my/rent-requests/$', MyRentRequestListView.as_view()),
                       url(r'^my/rents/$', MyRentListView.as_view()),
                       url(r'^my/donates/$', MyDonateListView.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^test/', include(urls.urlpatterns, namespace="core")),
                       url(r'^books/', include('bookshare.apps.books.urls')),
)

