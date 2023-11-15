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