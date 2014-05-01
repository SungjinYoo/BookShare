from django.shortcuts import render

import models

# Create your views here.
def index(request):
    context = {
        "books": models.Book.objects.all()
    }
    return render(request, "index.html", context)


def book(request, book_id):
    book = models.Book.objects.get(id=book_id)
    context = {
        "book": book
    }
    return render(request, "book.html", context)
