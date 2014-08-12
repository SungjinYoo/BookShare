#-*- coding:utf-8 -*-

import itertools

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

isbn_validator = RegexValidator(regex='^\d{13}$', message='Length has to be 13', code='nomatch')

class Course(models.Model):
    title = models.CharField(max_length=20)
    year = models.IntegerField()
    
    def __unicode__(self):
        return u"{} - {}".format(self.title, self.year)

class Book(models.Model):
    courses = models.ManyToManyField(Course)
    title = models.CharField(max_length=80)
    isbn = models.CharField(validators=[isbn_validator], max_length=13)
    
    # set upload_to in initializer
    image = models.ImageField(upload_to='images/books/')
    
    def __unicode__(self):
        return self.title

    def available_stock(self):
        return self.stock_set.available().order_by('condition').all()

    def any_availiable_stock(self):
        try:
            return list(self.available_stock()).pop()
        except IndexError:
            return None

    def rented_stock(self):
        return self.stock_set.rented().all()

    def rent_request(self):
        return self.rentrequest_set.pending().all()

    def done_request(self):
        return self.rentrequest_set.done().all()
    
    def canceled_request(self):
        return self.rentrequest_set.canceled().all()

    def point(self):
        return 1
