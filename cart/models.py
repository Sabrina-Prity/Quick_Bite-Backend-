from django.db import models
from django.contrib.auth.models import User
from food.models import FoodItem
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.food_item.name} | Quantity: {self.quantity}"