from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from drone_cones.models import *
import json


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=46, required=True, help_text='Enter your unique username.')
    first_name = forms.CharField(max_length=46, required=True)
    last_name = forms.CharField(max_length=46, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1')

class DroneRegisterForm(forms.Form):
    drone_name = forms.CharField(label="drone_name", max_length = 100)
    drone_size = forms.CharField(label="drone_size", max_length = 100)

class OrderForm(forms.Form):
    #items = forms.CharField(label = "items", max_length=1024)
    address = forms.CharField(label = "address", max_length=30)
    address2 = forms.CharField(label = "address2", max_length=30, required=False)
    city = forms.CharField(label = "city", max_length=30)
    state = forms.CharField(label = "state", max_length=30)
    zip = forms.IntegerField(label = "zip")
    timeOrdered = models.TimeField()
    timeDelivered = models.TimeField()
    timeToDeliver = models.TimeField()

class EditAccountForm(forms.Form):
    username = forms.CharField(label = "username", max_length=100)
    first_name = forms.CharField(label = "first_name", max_length=100)
    last_name = forms.CharField(label = "last_name", max_length=100)

class EditAddressForm(forms.Form):
    address_1 = forms.CharField(label="address_1", max_length = 100)
    address_2 = forms.CharField(label="address_2", max_length = 100, required=False)
    city = forms.CharField(label="city", max_length = 100)
    state = forms.CharField(label="state", max_length=100)
    zip = forms.CharField(label="zip", max_length = 100)

class EditDroneForm(forms.Form):
    drone_name = forms.CharField(label="drone_name", max_length = 100)
    drone_size = forms.CharField(label="drone_size", max_length = 100)
    is_active = forms.BooleanField(label="is_active", required=False)

class EditUserManagerForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    first_name = forms.CharField(label="first_name", max_length=100)
    last_name = forms.CharField(label="last_name", max_length=100)
    is_manager = forms.BooleanField(label="is_manager", required=False)

class EditStock(forms.Form):
    stockAvailable = forms.IntegerField(label="stockAvailable")
