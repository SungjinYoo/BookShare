#-*- coding:utf-8 -*-

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


class StockManager(models.Manager):
    def available(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=Stock.AVAILABLE)

    def rented(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=Stock.RENTED)

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
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="renting_stocks")
    book = models.ForeignKey(Book)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=AVAILABLE)

    objects = StockManager()

    def __unicode__(self):
        return u"{} [{}] - {}".format(self.book, self.id, self.owner)

    def ensure_status(self, status):
        assert self.status == status, "invalid status"

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


class RequestManager(models.Manager):
    def pending(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=RequestMixin.PENDING)
    
    def done(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=RequestMixin.DONE)
    
    def canceled(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs.filter(status=RequestMixin.CANCELED)

class RequestMixin(models.Model):
    class Meta:
        abstract = True
        ordering = ['-added_at']

    PENDING = u'pending'
    DONE = u'done'
    CANCELED = u'canceled'
    
    STATUS = (
        (PENDING, u'대기중'),
        (DONE, u'완료'),
        (CANCELED, u'취소')
    )

    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_(u'상태'), max_length=10,
                           choices=STATUS,
                           default=PENDING)

    objects = RequestManager()

    def __unicode__(self):
        return u"{} - {}".format(self.book, self.actor)

    def ensure_status(self, status):
        assert self.status == status, "invalid status"


class RentRequest(RequestMixin):
    book = models.ForeignKey(Book)

class ReturnRequest(RequestMixin):
    stock = models.ForeignKey(Stock)

class ReclaimRequest(RequestMixin):
    stock = models.ForeignKey(Stock)

def make_rent_request(actor, book):
    # check for user have multiple request for same book
    assert not RentRequest.objects.pending().filter(actor=actor, book=book)

    RentRequest.objects.create(actor=actor, book=book).save()

def cancel_rent_request(actor, rent_request):
    assert rent_request.actor == actor
    assert rent_request.status == RentRequest.PENDING

    rent_request.status = RentRequest.CANCELED
    rent_request.save()

def make_return_request(actor, stock):
    ReturnRequest.objects.create(actor=actor, stock=stock).save()

def cancel_return_request(actor, return_request):
    assert return_request.actor == actor
    return_request.delete()

@transaction.atomic
def process_rent_request(request):
    ### precondition
    request.ensure_status(RentRequest.PENDING)
    request.actor.ensure_points(request.book.point())
    assert request.book.any_availiable_stock()

    request.status = RentRequest.DONE

    stock = request.book.any_availiable_stock()
    stock.renter = request.actor
    stock.status = Stock.RENTED
    stock.save()

    StockHistory.objects.create(actor=request.actor,
                                stock=stock,
                                action=StockHistory.RENT,
                                condition=stock.condition).save()

    request.actor.lose_points(request.book.point())
    request.actor.save()
    request.save()

@transaction.atomic
def return_stock(actor, stock, condition):
    ### precondition
    stock.ensure_status(Stock.RENTED)

    stock.status = Stock.AVAILABLE
    stock.renter = None
    stock.save()
    StockHistory.objects.create(actor=actor,
                                stock=stock,
                                action=StockHistory.RETURN,
                                condition=condition).save()

@transaction.atomic
def deliver_stock(actor, book, condition):
    s = Stock.objects.create(owner=actor, book=book, condition=condition, renter=None)
    s.save()
    StockHistory.objects.create(actor=actor,
                                stock=s,
                                action=StockHistory.DELIVER,
                                condition=condition).save()

    actor.get_points(book.point())
    actor.save()

def request_reclaim(actor, stock):
    ### precondition
    stock.ensure_status(Stock.AVAILABLE)
    assert stock in actor.stock_set.all()

    ReclaimRequest.objects.create(actor=actor, stock=stock).save()

@transaction.atomic
def process_reclaim_request(request):
    ### precondition
    assert request.stock.owner == request.actor
    request.status.ensure_status(ReclaimRequest.PENDING)

    request.status = ReclaimRequest.DONE
    request.save()

    request.stock.status = Stock.RECLAIMED
    request.stock.save()

    StockHistory.objects.create(actor=request.actor,
                                stock=request.stock,
                                action=StockHistory.RECLAIM,
                                condition=request.stock.condition).save()

