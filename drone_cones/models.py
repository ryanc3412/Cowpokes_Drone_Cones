from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Id = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    cart = models.JSONField(default=list)
    is_admin = models.BooleanField(default=False)

class Drone(models.Model):
    TYPE_CHOICES = [
        ('large','Large'),
        ('medium','Medium'),
        ('small','Small')
    ]
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    droneName = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=TYPE_CHOICES)
    scoops = models.IntegerField()
    isActive = models.BooleanField(default = False)
    isDelivering = models.BooleanField(default = False)
    revenue = models.FloatField(default = 0)
    orders_delivered = models.IntegerField(default = 0)
    dateRegistered = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    items = models.JSONField(blank=True, null=True)
    drone = models.IntegerField(blank=True, null=True)
    orderCost = models.IntegerField(default=0)
    deliverySuccessful = models.BooleanField(blank=True, null=True)
    timeOrdered = models.TimeField(blank=True, null=True)
    timeDelivered = models.TimeField(blank=True, null=True)
    timeToDeliver = models.TimeField(blank=True, null=True)

class Products(models.Model):
    TYPE_CHOICES = [
        ('Ice Cream', 'Ice Cream'),
        ('Cone', 'Cone'),
        ('Topping', 'Topping')
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    image = models.ImageField(null=True, blank=True)
    flavor = models.CharField(max_length=100)
    stockAvailable = models.IntegerField()
    cost = models.FloatField(default=0.0)
    companyCost = models.FloatField(default=0.0)
    netRevenue = models.FloatField(default=0.0)
