# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name='full_date')
def full_date(time):
    return time.strftime("%Y년 %m월 %d일")
