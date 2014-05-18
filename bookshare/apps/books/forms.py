from django.contrib.auth import get_user_model
from django import forms

import models

class RentRequestForm(forms.Form):
    book = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=models.Book.objects.all())
