from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from cloudinary.models import CloudinaryField
# Create your models here.
DISTRICT_CHOICES = [
    ('barguna', 'Barguna'),
    ('barisal', 'Barisal'),
    ('bhola', 'Bhola'),
    ('jhalokati', 'Jhalokati'),
    ('patuakhali', 'Patuakhali'),
    ('pirojpur', 'Pirojpur'),
    ('bandarban', 'Bandarban'),
    ('brahmanbaria', 'Brahmanbaria'),
    ('chandpur', 'Chandpur'),
    ('chattogram', 'Chattogram'),
    ('coxsbazar', 'Cox\'s Bazar'),
    ('cumilla', 'Cumilla'),
    ('feni', 'Feni'),
    ('khagrachari', 'Khagrachari'),
    ('lakshmipur', 'Lakshmipur'),
    ('noakhali', 'Noakhali'),
    ('rangamati', 'Rangamati'),
    ('dhaka', 'Dhaka'),
    ('faridpur', 'Faridpur'),
    ('gazipur', 'Gazipur'),
    ('gopalganj', 'Gopalganj'),
    ('kishoreganj', 'Kishoreganj'),
    ('madaripur', 'Madaripur'),
    ('manikganj', 'Manikganj'),
    ('munshiganj', 'Munshiganj'),
    ('narayanganj', 'Narayanganj'),
    ('narsingdi', 'Narsingdi'),
    ('rajbari', 'Rajbari'),
    ('shariatpur', 'Shariatpur'),
    ('tangail', 'Tangail'),
    ('bagerhat', 'Bagerhat'),
    ('chuadanga', 'Chuadanga'),
    ('jashore', 'Jashore'),
    ('jhenaidah', 'Jhenaidah'),
    ('khulna', 'Khulna'),
    ('kushtia', 'Kushtia'),
    ('magura', 'Magura'),
    ('meherpur', 'Meherpur'),
    ('narail', 'Narail'),
    ('satkhira', 'Satkhira'),
    ('bogura', 'Bogura'),
    ('chapainawabganj', 'Chapainawabganj'),
    ('joypurhat', 'Joypurhat'),
    ('naogaon', 'Naogaon'),
    ('natore', 'Natore'),
    ('pabna', 'Pabna'),
    ('rajshahi', 'Rajshahi'),
    ('sirajganj', 'Sirajganj'),
    ('dinajpur', 'Dinajpur'),
    ('gaibandha', 'Gaibandha'),
    ('kurigram', 'Kurigram'),
    ('lalmonirhat', 'Lalmonirhat'),
    ('nilphamari', 'Nilphamari'),
    ('panchagarh', 'Panchagarh'),
    ('rangpur', 'Rangpur'),
    ('thakurgaon', 'Thakurgaon'),
    ('habiganj', 'Habiganj'),
    ('maulvibazar', 'Maulvibazar'),
    ('sunamganj', 'Sunamganj'),
    ('sylhet', 'Sylhet'),
]

class Seller(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='media/seller/', null=True, blank=True)
    # image = models.CharField(max_length=100, null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    company_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, default='Dhaka')
    mobile_no = models.CharField(max_length=12, unique=True)
    

    def __str__(self):
        return f"Name: {self.company_name}"


STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by : {self.user} "


