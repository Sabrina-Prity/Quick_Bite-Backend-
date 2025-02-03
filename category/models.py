from django.db import models
from seller.models import Seller
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name