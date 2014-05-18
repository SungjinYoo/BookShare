from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView

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

        query = Q()
        
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

class BookRentView(View):
    def get(self):
        return HttpResponseForbidden()

    def post(self):
        print self.request.POST
        #request_rent(self.request.user, None)
        return HttpResponse()
