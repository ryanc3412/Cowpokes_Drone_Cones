from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from drone_cones.models import *
import json


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=46, required=True, help_text='Optional.')
    first_name = forms.CharField(max_length=46, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=46, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    address = forms.CharField(max_length=150, required=True, help_text='Optional.')
    address2 = forms.CharField(max_length=150, required=False, help_text='Optional.')
    city = forms.CharField(max_length=189, required=True, help_text='Optional.')
    state = forms.CharField(max_length=189, required=True, help_text='Optional.')
    zip = forms.CharField(max_length=18, required=True, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'address2', 'city', 'state', 'zip', 'password1')

class DroneRegisterForm(forms.Form):
    drone_name = forms.CharField(label = "Drone Name", max_length=100)
    size = forms.CharField(label = "Size", max_length=100)
    scoops = forms.IntegerField(label = "Scoops")

class OrderForm(forms.Form):
    items = forms.CharField(max_length=1024)
    address = forms.CharField(max_length=30)
    address2 = forms.CharField(max_length=30)
    city = forms.CharField(max_length=30)
    state = forms.CharField(max_length=30)
    zip = forms.CharField(max_length=30)

    def clean_jsonfield(self):
         jdata = self.cleaned_data['jsonfield']
         try:
             json_data = json.loads(jdata) #loads string as json
             #validate json_data
         except:
             raise forms.ValidationError("Invalid data in jsonfield")
         #if json data not valid:
            #raise forms.ValidationError("Invalid data in jsonfield")
         return jdata

    class Meta:
        model = Orders
        fields = ('address', 'address2', 'city', 'state', 'zip', 'items')