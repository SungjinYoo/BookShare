#-*- coding:utf-8 -*-
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from bookshare.apps.core import models
from bookshare.apps.books import models as books_models
from bookshare.apps.users import models as users_models
import forms


# Create your views here.
def index(request):
    if request.method == "GET": 
        return render(request, "console/index.html")

def deliver_stock(request, book):
    if request.method == "GET":
        context = {
            "stock_form": forms.StockDeliverForm(initial={'book': book}),
            "book": books_models.Book.objects.get(id=book)
        }
        return render(request, "console/deliver_stock_form.html", context)

    if request.method == "POST":
        form = forms.StockDeliverForm(request.POST)
        if form.is_valid():
            models.deliver_stock(form.cleaned_data["actor"],
                                 form.cleaned_data["book"],
                                 form.cleaned_data["condition"])
            return redirect('console:index')

def process_rent_request(request, rent_request):
    if request.method == "GET":
        context = {
            "rent_request_form": forms.RentRequestProcessForm(initial={'request': rent_request}),
            "rent_request": models.RentRequest.objects.get(id=rent_request)
        }
        return render(request, "console/rent_request_confirm.html", context)

    if request.method == "POST":
        form = forms.RentRequestProcessForm(request.POST)
        if form.is_valid():
            models.process_rent_request(form.cleaned_data["request"])
            return redirect('console:rent_request_list')


def search_users(request):    
    if request.method == "GET":
        context = dict(
            user_list = users_models.User.objects.all(),
        )
        return render(request, "console/search_users.html", context)

    if request.method == "POST":
        user_name = request.POST.get('user_name', '')

        context = dict(
            user_list = users_models.User.objects.filter(name__icontains=user_name)
        )

        return render(request, "console/search_users.html", context)

    return HttpResponseForbidden()

def user_stock_list(request):
    if request.method == "GET":
        user_pk = request.GET.get('user_pk', None)
        if not user_pk :
            return HttpResponseForbidden()
        
        user = users_models.User.objects.get(id=user_pk)
        if not user:
            return HttpResponseForbidden()

            
        context = dict(
            user = user,
        )
    
        return render(request, 'console/user_stock_list.html', context)

def process_return_request(request):
    if request.method == "GET":
        user = users_models.User.objects.get(id=request.GET.get('user_pk'))
        stock = models.Stock.objects.get(id=request.GET.get('stock_pk'))
        
        if not user or not stock :
            return HttpResponseForbidden()

        context = dict(
            user = user,
            stock = stock,
            conditions = models.Stock.CONDITIONS,
        )
        
        return render(request, 'console/return_confirm.html', context)

    if request.method == "POST":
        form = forms.ReturnProcessForm(request.POST)
        
        if form.is_valid():
            models.return_stock(form.cleaned_data['user'],
                                form.cleaned_data['stock'],
                                form.cleaned_data['condition'])
            return redirect(reverse('console:search_users'))
        
class RentRequestListView(ListView):
    template_name = 'console/rent_request.html'
    queryset = models.RentRequest.objects.pending

class BookListView(ListView):
    template_name = 'console/deliver_stock.html'
    model = books_models.Book

class RentBookListView(ListView):
    template_name = 'console/rent_books.html'
    queryset = books_models.Book.objects.available

def add_book(request):
    form = forms.BookAddForm(request.POST or None)

    context = {
        "form": form
    }
    if request.method == "GET":
        return render(request, 'console/add_book.html', context)

    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            isbn = form.cleaned_data["isbn"]
            cover_url = form.cleaned_data["cover_url"]

            books_models.add_book(title, isbn, cover_url)
            return redirect(reverse('console:index'))

def rent_book(request, book=None):
    form = forms.BookRentForm(request.POST or None, initial={"book" : book})

    context = {
        "form": form
    }
    if request.method == "GET":
        book = books_models.Book.objects.get(id=book)
        context["book"] = book
        context["stock"] = book.any_availiable_stock()
        return render(request, 'console/rent_book.html', context)

    if request.method == "POST":
        if form.is_valid():
            book = form.cleaned_data["book"]
            user = form.cleaned_data["user"]
            
            models.rent_book(user, book)
            return redirect(reverse('console:index'))
