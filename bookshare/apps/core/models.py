from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class BookShareModel(models.Model):
    pub_date = models.DateTimeField(_('Published Date'), default=timezone.now, auto_now_add=True)
    class Meta:
        abstract = True
