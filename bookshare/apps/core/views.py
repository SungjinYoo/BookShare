
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

import forms
import models

# Create your views here.
def request_rent(request):
    if request.method == "GET":
        context = {
            "form": forms.RentRequestForm()
        }
        return render(request, "request_rent.html", context)

    if request.method == "POST":
        form = forms.RentRequestForm(request.POST)
        if form.is_valid():
            models.request_rent(form.cleaned_data["actor"], form.cleaned_data["book"])
            return redirect('books:index')

def deliver_stock(request):
    if request.method == "GET":
        context = {
            "form": forms.StockDeliverForm()
        }
        return render(request, "deliver_stock.html", context)

    if request.method == "POST":
        form = forms.StockDeliverForm(request.POST)
        if form.is_valid():
            models.deliver_stock(form.cleaned_data["actor"],
                                form.cleaned_data["book"],
                                form.cleaned_data["condition"])
            return redirect('books:index')

def process_rent_request(request):
    if request.method == "GET":
        context = {
            "form": forms.RentRequestProcessForm()
        }
        return render(request, "process_rent_request.html", context)

    if request.method == "POST":
        form = forms.RentRequestProcessForm(request.POST)
        if form.is_valid():
            models.process_rent_request(form.cleaned_data["request"])
            return redirect('books:index')
