from django.contrib.auth import get_user_model
from django import forms

from bookshare.apps.core import models

from bookshare.apps import books

class StockDeliverForm(forms.Form):
    actor = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    book = forms.ModelChoiceField(queryset=books.models.Book.objects.all())
    condition = forms.ChoiceField(choices=models.Stock.CONDITIONS)

