from django.contrib.auth import get_user_model
from django import forms

import models
from bookshare.apps.core.models import Stock, RentRequest, ReturnRequest

class RentRequestForm(forms.Form):
    book = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=models.Book.objects.all())


class CancelRentRequestForm(forms.Form):
    rent_request = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                         queryset=RentRequest.objects.all())

class ReturnRequestForm(forms.Form):
    stock = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                   queryset=Stock.objects.all())

class CancelReturnRequest(forms.Form):
    return_request = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                            queryset=ReturnRequest.objects.all())
