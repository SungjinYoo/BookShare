from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from models import Book

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
        # need pagination?
        return Book.objects.filter(Q(title__icontains=title) |
                                   Q(courses__department__icontains=department))

        
