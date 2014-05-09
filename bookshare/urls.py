from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'bookshare.views.index'),
                       url(r'^signin/$', 'bookshare.views.signin'),
                       url(r'^signup/$', 'bookshare.views.signup'),
                       url(r'^signout/$', 'bookshare.views.signout'),
                       url(r'^admin/', include(admin.site.urls)),
)
