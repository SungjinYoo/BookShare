#encoding=utf8

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bookshare.apps.books.models import Book

User = get_user_model()

class BookShareModel(models.Model):
    pub_date = models.DateTimeField(_('Published Date'), default=timezone.now, auto_now_add=True)
    class Meta:
        abstract = True

class Stock(models.Model):
    AVAILABLE = u'available'
    RENTED = u'rented'
    
    STATUS = (
        (AVAILABLE, u'대여 가능'),
        (RENTED, u'대여중'),
    )

    owner = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=AVAILABLE)
