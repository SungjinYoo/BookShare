from django.db.models import Q
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView

import forms
from models import Book

from bookshare.apps.core.models import request_rent


# Create your views here.
def index(request):
    context = {
        "books": models.Book.objects.all()
    }
    return render(request, "index.html", context)

class BookDetailView(DetailView):
    model = Book

class BookSearchView(ListView):
    template_name = 'books/book_search.html'

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        department = self.request.GET.get('department', '')

        query = None
        
        if title :
            print 'title'
            query |= Q(title__icontains=title)
        if department :
            print 'department'
            query |= Q(courses__department__icontains=department)

        # need pagination?        
        if query :
            return Book.objects.filter(query)
        else :
            # just empty list? or all the books?
            return Book.objects.all()

        
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['rent_request_form'] = forms.RentRequestForm(initial={'book': context["object"].pk})
        return context

def rent_request(request):
    if request.method == "POST":
        form = forms.RentRequestForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated():
                request_rent(request.user, form.cleaned_data["book"])
                return render(request, "books/rent_request_complete.html")
            else:
                next_url = reverse_lazy("book-detail", kwargs={"pk": request.POST.get("book", None)})
                return redirect(reverse_lazy("signin_next", kwargs={"next": next_url}))

