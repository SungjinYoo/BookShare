from django.contrib.auth import get_user_model
from django import forms

import models
from bookshare.apps.core.models import RentRequest

class RentRequestForm(forms.Form):
    book = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=models.Book.objects.all())


class CancelRentRequestForm(forms.Form):
    rentrequest = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                         queryset=RentRequest.objects.all())
