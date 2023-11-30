from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

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
    cart = models.JSONField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

class Drone(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    droneName = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    scoops = models.IntegerField()
    isActive = models.BooleanField(default = False)
    dateRegistered = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    items = models.JSONField(blank=True, null=True)
    drone = models.IntegerField(blank=True, null=True)
    deliverySuccessful = models.BooleanField(blank=True, null=True)
    timeOrdered = models.TimeField(blank=True, null=True)
    timeDelivered = models.TimeField(blank=True, null=True)
    timeToDeliver = models.TimeField(blank=True, null=True)

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    stockAvailable = models.IntegerField()
