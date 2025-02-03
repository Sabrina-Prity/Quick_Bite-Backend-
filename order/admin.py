from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['food_items', 'quantity','buying_status', 'created_at']
    filter_horizontal = ('food_items',)
    def name(self,obj):
        return obj.food_items.name
    
    
    
admin.site.register(Order)
admin.site.register(OrderItem)