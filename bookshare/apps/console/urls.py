from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    url(r'^$', views.index, name='index'),
    #url(r'stock$', views.ListView, name='stock_list'),
    url(r'^/books$', views.BookListView.as_view(), name='books'),
    url(r'^/books/([0-9]+)/stock/add$', views.deliver_stock, name="deliver_stock"),
    url(r'^/books/add$', views.add_book, name='add_book'),
    url(r'^/rent$', views.RentBookListView.as_view(), name='rent_book_list'),
    url(r'^/books/([0-9]+)/rent$', views.rent_book, name='rent_book'),
    url(r'^/search-users/$', views.search_users, name='search_users'),
    url(r'^/user-stock-list/$', views.user_stock_list, name='user_stock_list'),
    url(r'^/return-request/$', views.process_return_request, name='process_return_request'),
    url(r'^/user/add$', views.SignUpView.as_view(), name='user_add'),
    url(r'^/bulk$', views.bulk_add, name='bulk_add'),
    url(r'^/add-book-and-stock$', views.add_book_and_stock, name='add_book_and_stock'),
    url(r'^/stocks$', views.stocks, name='stocks'),
    # url(r'^/get_user$', views.get_user, name='get_user'),                       
)

