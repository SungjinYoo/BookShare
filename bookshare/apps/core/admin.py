from django.contrib import admin
from models import Stock

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'owner', 'changed_at', )
    list_filter = ('status', 'owner', )

admin.site.register(Stock, StockAdmin)
