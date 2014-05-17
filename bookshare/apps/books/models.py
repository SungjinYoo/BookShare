#encoding=utf8

import itertools

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

isbn_validator = RegexValidator(regex='^\d{13}$', message='Length has to be 13', code='nomatch')

class Course(models.Model):
    SPRING = u'spring'
    SUMMER = u'summer'
    FALL = u'fall'
    WINTER = u'winter'

    SEMESTERS = (
        (SPRING, u'봄'),
        (SUMMER, u'여름'),
        (FALL, u'가을'),
        (WINTER, u'겨울')
    )

    title = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    year = models.IntegerField()
    semester = models.CharField(_(u'학기'), max_length=10,
                           choices=SEMESTERS,
                           default=SPRING)

    def __unicode__(self):
        return u"{} - {} {}".format(self.title, self.year, self.semester)

class Book(models.Model):
    courses = models.ManyToManyField(Course)
    title = models.CharField(max_length=80)
    isbn = models.CharField(validators=[isbn_validator], max_length=13)
    
    # set upload_to in initializer
    image = models.ImageField(upload_to=settings.MEDIA_ROOT)
    
    def __unicode__(self):
        return str(self).decode('utf-8')

    def __str__(self):
        return self.title

    def available_stock(self):
        return self.stock_set.available().order_by('condition').all()

    def any_availiable_stock(self):
        try:
            return list(self.available_stock()).pop()
        except IndexError:
            return None

    def point(self):
        return 1
