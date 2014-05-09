# -*- coding:utf-8 -*- 
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, user_id, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(user_id=user_id,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, **extra_fields):
        u = self.create_user(user_id, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class BookShareAbstractUser(AbstractBaseUser):
    MALE = 'M'
    FEMALE = 'F'

    MALE_FEMALE_CHOICES = (
        (MALE, u'남'),
        (FEMALE, u'여')
    )

    user_id = models.CharField(_(u'아이디'), 
                               max_length=15, 
                               help_text=_(u'사용자 아이디'),
                               unique=True,
                               db_index=True)
    
    name = models.CharField(_(u'이름'), 
                               max_length=15, 
                               help_text=_(u'이름'))
    
    email = models.EmailField(_('Email (ID)'),
                              max_length=255,
                              db_index=True,
                              unique=True)
    
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as'
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = models.CharField(_(u'전화번호'),
                                    max_length=20,
                                    null=True)

    # detail profile
    sex = models.CharField(_(u'성별'), max_length=1,
                           choices=MALE_FEMALE_CHOICES,
                           default='M')
    age = models.IntegerField(_(u'나이'), blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _(u'사용자')
        verbose_name_plural = _(u'사용자')
        abstract = True

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def __unicode__(self):
        return self.email

class User(BookShareAbstractUser):
    class Meta:
        verbose_name = _(u'서비스 유저')
        verbose_name_plural = _(u'서비스 유저들')
        swappable = 'AUTH_USER_MODEL'
