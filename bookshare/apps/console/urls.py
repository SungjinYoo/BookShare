from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'^$', views.index, name='index'),
    #url(r'stock$', views.ListView, name='stock_list'),
    url(r'/books$', views.BookListView.as_view(), name='books'),
    url(r'/books/([0-9]+)/stock/add', views.deliver_stock, name="deliver_stock"),
    url(r'/books/add$', views.add_book, name='add_book'),
    url(r'/rent-request$', views.RentRequestListView.as_view(), name='rent_request_list'),
    url(r'/rent-request/([0-9]+)/process$', views.process_rent_request, name='process_rent_req'),
    url(r'/search-users/$', views.search_users, name='search_users'),
    url(r'/user-stock-list/$', views.user_stock_list, name='user_stock_list'),
    url(r'/return-request/$', views.process_return_request, name='process_return_request'),
)

