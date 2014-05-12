from django.shortcuts import render

import models

# Create your views here.
def index(request):
    context = {
        "books": models.Book.objects.all()
    }
    return render(request, "index.html", context)


from django.views.generic.detail import DetailView

from models import Book

class BookDetailView(DetailView):
    model = Book
