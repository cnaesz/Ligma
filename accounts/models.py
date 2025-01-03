from symtable import Class

from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField( null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.get_username()
        return 'Anonymous'

class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    CATEGORY = (
        ('Classic', 'Classic'),
        ('Sports', 'Sports'),
        ('Minimal', 'Minimal'),
    )
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(max_length=100, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY, null=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('on the way!', 'On the Way!'),
        ('delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name