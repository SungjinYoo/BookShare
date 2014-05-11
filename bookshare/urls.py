from django.conf.urls import patterns, include, url

from bookshare.views import MyPageView

from django.contrib import admin

from bookshare.views import SignInView, SignUpView
from bookshare.apps.core import urls
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'bookshare.views.index'),
                       url(r'^signin/$', SignInView.as_view()),
                       url(r'^signup/$', SignUpView.as_view()),
                       url(r'^signout/$', 'bookshare.views.signout'),
                       url(r'^me/$', MyPageView.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^test/', include(urls.urlpatterns, namespace="core")),
)
