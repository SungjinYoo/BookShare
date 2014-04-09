# -*- coding:utf-8 -*- 
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class BookShareAbstractUser(AbstractBaseUser):
    MALE = 'M'
    FEMALE = 'F'

    MALE_FEMALE_CHOICES = (
        (MALE, u'남'),
        (FEMALE, u'여')
    )

    is_active = models.BooleanField(default=True)
    user_name = models.CharField(max_length=255)
    sex = models.CharField(_(u'성별'), max_length=1,
                           choices=MALE_FEMALE_CHOICES,
                           default='M')
    age = models.IntegerField(_(u'나이'), blank=True, null=True)
    email = models.EmailField(_('Email'),
                              max_length=255,
                              db_index=True,
                              unique=True)

    last_login_date = models.DateTimeField(_('last login'), default=timezone.now)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_name']
    
    def get_full_name(self):
        return self.user_name
        
    def get_email(self):
        return self.email
        
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.user_name

class User(BookShareAbstractUser):
    class Meta:
        verbose_name = _(u'서비스 유저')
        verbose_name_plural = _(u'서비스 유저들')
