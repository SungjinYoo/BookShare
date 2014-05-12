from django.shortcuts import render
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
