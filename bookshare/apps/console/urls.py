from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'^$', views.index, name='index'),
    #url(r'stock$', views.ListView, name='stock_list'),
    url(r'stock/add$', views.deliver_stock, name='deliver_stock'),
    url(r'rent-request$', views.RentRequestListView.as_view(), name='rent_request_list'),
    url(r'rent-request/([0-9]+)/process$', views.process_rent_request, name='process_rent_req'),
)
