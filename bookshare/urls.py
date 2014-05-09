from django.conf.urls import patterns, include, url

from django.contrib import admin

from bookshare.views import SignInView
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'bookshare.views.index'),
                       # url(r'^signin/$', 'bookshare.views.signin'),
                       url(r'^signin/$', SignInView.as_view()),
                       url(r'^signup/$', 'bookshare.views.signup'),
                       url(r'^signout/$', 'bookshare.views.signout'),
                       url(r'^admin/', include(admin.site.urls)),
)
