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
    items = forms.CharField(label = "Items", max_length=1024)
    address = forms.CharField(label = "address", max_length=30)
    address2 = forms.CharField(label = "address2", max_length=30)
    city = forms.CharField(label = "city", max_length=30)
    state = forms.CharField(label = "state", max_length=30)
    zip = forms.CharField(label = "zip", max_length=30)