from django.shortcuts import render, redirect
from django.views.generic import ListView
from bookshare.apps.core import models
from bookshare.apps.books import models as books_models
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

class RentRequestListView(ListView):
    template_name = 'console/rent_request.html'
    model = models.RentRequest

class BookListView(ListView):
    template_name = 'console/deliver_stock.html'
    model = books_models.Book
