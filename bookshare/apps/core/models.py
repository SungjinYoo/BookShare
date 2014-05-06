#encoding=utf8

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bookshare.apps.books.models import Book

class BookShareModel(models.Model):
    pub_date = models.DateTimeField(_('Published Date'), default=timezone.now, auto_now_add=True)
    class Meta:
        abstract = True


class ConditionMixin(models.Model):
    class Meta:
        abstract = True

    A = "A"
    B = "B"
    C = "C"

    CONDITIONS = (
        (A, "A"),
        (B, "B"),
        (C, "C"),
    )

    condition = models.CharField(_(u'보관상태'), max_length=2, choices=CONDITIONS)


class StockAvailableManager(models.Manager):
    def available(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=Stock.AVAILABLE)


class Stock(ConditionMixin):
    AVAILABLE = u'available'
    RENTED = u'rented'
    RECLAIMED = u'reclaimed'
    
    STATUS = (
        (AVAILABLE, u'대여 가능'),
        (RENTED, u'대여중'),
        (RECLAIMED, u'반환 완료'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=AVAILABLE)

    objects = StockAvailableManager()

    def __unicode__(self):
        return u"{} [{}] - {}".format(self.book, self.id, self.owner)

class StockHistory(ConditionMixin):
    RENT = u'rent'
    RETURN = u'return'
    DELIVER = u'deliver'
    RECLAIM = u'reclaim'
    
    ACTION = (
        (RENT, u'대여'),
        (RETURN, u'반납'),
        (DELIVER, u'위탁'),
        (RECLAIM, u'반환'),
    )

    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    stock = models.ForeignKey(Stock)
    added_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(_(u'행동'), max_length=10, choices=ACTION)


class RentRequestPendingManager(models.Manager):
    def pending(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=RentRequest.PENDING)


class RentRequest(models.Model):
    PENDING = u'pending'
    DONE = u'done'
    CANCELED = u'canceled'
    
    STATUS = (
        (PENDING, u'대기중'),
        (DONE, u'완료'),
        (CANCELED, u'취소')
    )

    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=PENDING)

    objects = RentRequestPendingManager()

    def __unicode__(self):
        return u"{} - {}".format(self.book, self.actor)


class ReclaimRequest(models.Model):
    PENDING = u'pending'
    DONE = u'done'
    CANCELED = u'canceled'
    
    STATUS = (
        (PENDING, u'대기중'),
        (DONE, u'완료'),
        (CANCELED, u'취소')
    )

    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    stock = models.ForeignKey(Stock)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=PENDING)


def request_rent(actor, book):
    ### precondition
    # stock.status == Stock.AVAILABLE
    
    RentRequest.objects.create(actor=actor, book=book).save()

@transaction.atomic
def process_rent_request(request):
    ### precondition
    # request.stock.status == Stock.AVAILABLE 
    # request.status == RentRequest.PENDING
    # request.actor.point >= request.stock.book.point

    request.status = RentRequest.DONE
    request.save()

    stock = request.book.available_stock()[0]

    stock.status = Stock.RENTED
    stock.save()

    StockHistory.objects.create(actor=request.actor,
                                stock=stock,
                                action=StockHistory.RENT,
                                condition=stock.condition).save()

    # take point from request.actor, depending on stock.book

@transaction.atomic
def return_stock(actor, stock, condition):
    ### precondition
    # stock.status == Stock.RENTED

    stock.status = Stock.AVAILABLE
    stock.save()
    StockHistory.objects.create(actor=actor,
                                stock=stock,
                                action=StockHistory.RETURN,
                                condition=condition).save()

@transaction.atomic
def deliver_stock(actor, book, condition):
    s = Stock.objects.create(owner=actor, book=book, condition=condition)
    s.save()
    StockHistory.objects.create(actor=actor,
                                stock=s,
                                action=StockHistory.DELIVER,
                                condition=condition).save()

    # give point to request.actor depending on book

def request_reclaim(actor, stock):
    ### precondition
    # request.stock.status == Stock.AVAILABLE

    ReclaimRequest.objects.create(actor=actor, stock=stock).save()

@transaction.atomic
def process_reclaim_request(request):
    ### precondition
    # request.stock.status == Stock.AVAILABLE
    # request.status == ReclaimRequest.PENDING

    request.status = ReclaimRequest.DONE
    request.save()

    request.stock.status = Stock.RECLAIMED
    request.stock.save()

    StockHistory.objects.create(actor=request.actor,
                                stock=request.stock,
                                action=StockHistory.RECLAIM,
                                condition=request.stock.condition).save()

