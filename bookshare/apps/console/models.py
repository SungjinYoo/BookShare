from django.db import models
from bookshare.apps.books import models as books_models
from bookshare.apps.core.models import deliver_stock

# Create your models here.
def add_book_and_stock(user, isbn, condition):
    try:
        book = books_models.Book.objects.filter(isbn=isbn.strip())[0]
        deliver_stock(user, book, condition)
    except:
        pass
