from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^book/([0-9]+)$', views.book, name='book'),
)
