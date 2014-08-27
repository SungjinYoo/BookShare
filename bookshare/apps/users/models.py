# -*- coding:utf-8 -*- 
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, user_id, name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        user = self.model(user_id = user_id, name = name,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, password, **extra_fields):
        u = self.create_user(user_id, name, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class BookShareAbstractUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(_(u'학번'), 
                               max_length=10, 
                               help_text=_(u'학번'),
                               unique=True,
                               db_index=True)
    
    name = models.CharField(_(u'이름'), 
                               max_length=15, 
                               help_text=_(u'이름'))
    
    email = models.EmailField(_('Email'),
                              max_length=255,
                              unique=True)
    
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as'
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = models.CharField(_(u'연락처'),
                                    max_length=20)

    objects = UserManager()
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'user_id'
    
    class Meta:
        verbose_name = _(u'사용자')
        verbose_name_plural = _(u'사용자')
        abstract = True

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.phone_number)

class User(BookShareAbstractUser):
    class Meta:
        verbose_name = _(u'서비스 유저')
        verbose_name_plural = _(u'서비스 유저들')
        swappable = 'AUTH_USER_MODEL'

    points = models.IntegerField(default=0)

    def ensure_points(self, points):
        assert self.points >= points, "포인트가 부족합니다"

    def get_points(self, points):
        assert points > 0, "포인트는 0 이하로 떨어질 수 없습니다"
        self.points += points

    def lose_points(self, points):
        assert points > 0, "포인트가 0 이하로 떨어질 수 없습니다"
        self.ensure_points(points)
        self.points -= points
