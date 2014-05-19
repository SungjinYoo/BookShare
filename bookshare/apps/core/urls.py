from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'request_rent$', views.request_rent, name='request_rent'),
    url(r'process_rent_request$', views.process_rent_request, name='process_rent_req'),
    url(r'deliver_stock$', views.deliver_stock, name='deliver_stock'),
)
