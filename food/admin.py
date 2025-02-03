from django.contrib import admin
from .models import FoodItem, Comment
# Register your models here.


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'image']
    search_fields = ['name', 'category__name']
    list_filter = ['category']

admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Comment)