from django.db import models
from seller.models import Seller
from django.contrib.auth.models import User
from category.models import Category
from cloudinary.models import CloudinaryField


# Create your models here.
class FoodItem(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="food_items")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"Food Item: {self.name} - Price:{self.price}"
    

STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by : {self.user}"