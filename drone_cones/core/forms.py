from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from drone_cones.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class DroneRegisterForm(forms.Form):
    drone_name = forms.CharField(label = "Drone Name", max_length=100)
    size = forms.CharField(label = "Size", max_length=100)
    scoops = forms.IntegerField(label = "Scoops")

class OrderForm(forms.Form):
    #items = forms.CharField(label = "items", max_length=1024)
    address = forms.CharField(label = "address", max_length=30)
    address2 = forms.CharField(label = "address2", max_length=30)
    city = forms.CharField(label = "city", max_length=30)
    state = forms.CharField(label = "state", max_length=30)
    zip = forms.IntegerField(label = "zip")

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
    drone_capacity = forms.IntegerField(label="drone_capacity")