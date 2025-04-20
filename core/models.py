# models.py

from django.db import models
#from PIL import Image
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Product(models.Model):
    name = models.CharField(max_length=55,null=False,blank=False)
    unit_price = models.PositiveIntegerField(default=1)
    seller = models.CharField(max_length=55,blank=False,null=False)
    image = models.ImageField(upload_to='product_images')
    
    def __str__(self):
        return self.name

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # optional: to track when the message was sent
    status = models.BooleanField(max_length=55,default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Order(models.Model):
    item_name = models.CharField(max_length=255)
    item_id = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"