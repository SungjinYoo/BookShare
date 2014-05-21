#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView

import forms
from models import Book

from bookshare.apps.core.models import request_rent
from bookshare.settings.base import LOGIN_URL

# Create your views here.
def index(request):
    context = {
        "books": models.Book.objects.all()
    }
    return render(request, "index.html", context)

class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['rent_request_form'] = forms.RentRequestForm(initial={'book': context["object"].pk})
        return context

class BookSearchView(ListView):
    template_name = 'books/book_search.html'

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        department = self.request.GET.get('department', '')

        query = Q()
        
        if title :
            query |= Q(title__icontains=title)
        if department :
            query |= Q(courses__department__icontains=department)

        # need pagination?        
        if query :
            return Book.objects.filter(query)
        else :
            # just empty list? or all the books?
            return Book.objects.all()


#login required is in the code explicitly
def rent_request(request):
    if not request.user.is_authenticated():
        return redirect(LOGIN_URL)

    if request.method == "POST":
        form = forms.RentRequestForm(request.POST)

        if form.is_valid():
            request_rent(request.user, form.cleaned_data["book"])
            return render(request, "books/rent_request_complete.html")

    else :
        return HttpResponseForbidden()
