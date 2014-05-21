from django.contrib import admin
from models import Stock, RentRequest, ReclaimRequest, StockHistory

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'owner', 'changed_at', 'condition', )
    list_filter = ('status', 'owner', )

class RentRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'actor', 'status', 'changed_at')
    list_filter = ('status', 'actor', )

class ReclaimRequestAdmin(admin.ModelAdmin):
    list_display = ('stock', 'actor', 'status', 'changed_at')
    list_filter = ('status', 'actor', )

class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('actor', 'stock', 'action', 'added_at', 'condition',)
    list_filter = ('actor', 'action', )


admin.site.register(Stock, StockAdmin)
admin.site.register(RentRequest, RentRequestAdmin)
admin.site.register(ReclaimRequest, ReclaimRequestAdmin)
admin.site.register(StockHistory, StockHistoryAdmin)
