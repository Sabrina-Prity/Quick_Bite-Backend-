from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import CartItem,Cart

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity')
    


    
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart)
