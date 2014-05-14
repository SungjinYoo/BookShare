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

def rent_request(request, pk=None):
    return render(request, "books/rent_request_complete.html")
