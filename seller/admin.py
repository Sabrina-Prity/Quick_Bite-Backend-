from django.contrib import admin
from .models import Seller, Review


# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'street_name', 'district', 'postal_code')
    search_fields = ('company_name', 'street_name', 'district')
admin.site.register(Seller, SellerAdmin)
admin.site.register(Review)