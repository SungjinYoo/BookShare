#encoding=utf8

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

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    AVAILIABLE = 'available'
    RENTED = 'rented'

    BOOKINSTANCE_STATUS = (
        (AVAILIABLE, u'대여 가능'),
        (RENTED, u'대여 중'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book)
    imported_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'대여 상태'), max_length=10,
                           choices=BOOKINSTANCE_STATUS,
                           default=AVAILIABLE)
