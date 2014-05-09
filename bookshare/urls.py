from django.conf.urls import patterns, include, url

from django.contrib import admin

from bookshare.views import SignInView, SignUpView
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'bookshare.views.index'),
                       url(r'^signin/$', SignInView.as_view()),
                       url(r'^signup/$', SignUpView.as_view()),
                       url(r'^signout/$', 'bookshare.views.signout'),
                       url(r'^admin/', include(admin.site.urls)),
)
