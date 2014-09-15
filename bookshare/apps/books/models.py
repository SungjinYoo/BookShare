#-*- coding:utf-8 -*-

import itertools
from urlparse import urlparse 

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import requests

isbn_validator = RegexValidator(regex='^\d{13}$', message='Length has to be 13', code='nomatch')

class Course(models.Model):
    FIRST = u'first'
    SUMMER = u'summer'
    SECOND = u'second'
    WINTER = u'winter'

    SEMESTERS = (
        (FIRST, u'1학기'),
        (SUMMER, u'여름'),
        (SECOND, u'2학기'),
        (WINTER, u'겨울')
    )

    title = models.CharField(max_length=20)
    department = models.CharField(blank=True, max_length=20)
    year = models.IntegerField(default=2014)
    semester = models.CharField(_(u'학기'),
                                blank=True,
                                max_length=10,
                                choices=SEMESTERS,
                                default=SECOND)
    

    def __unicode__(self):
        return u"{} - {} {}".format(self.title, self.year, self.semester)

class BookManager(models.Manager):
    def available(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.exclude(stock=None)

class Book(models.Model):
    courses = models.ManyToManyField(Course, blank=True)
    title = models.CharField(max_length=80)
    isbn = models.CharField(validators=[isbn_validator], max_length=13)
    
    # set upload_to in initializer
    image = models.ImageField(upload_to='images/books/')
    
    objects = BookManager()
    
    def __unicode__(self):
        return self.title

    def available_stock(self):
        return self.stock_set.available().order_by('condition')

    def num_available_stocks(self):
        return len(self.stock_set.available())

    def any_availiable_stock(self):
        try:
            return self.available_stock()[0]
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

def add_book(title, isbn, cover_url):
    cover_url_resp = requests.get(cover_url, stream=True)
    if cover_url_resp.ok and "image" in cover_url_resp.headers["content-type"]:
        book = Book(isbn=isbn, title=title)

        o = urlparse(cover_url_resp.request.url)
        filename = o.path.split("/")[-1]

        book.image.save(filename, ContentFile(cover_url_resp.content))
        book.save()

        return book

