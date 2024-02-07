from django import forms
from .models import Order
from accounts.models import Address




# forms.py


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name','phone_number','address_line_1','address_line_2','city','state','country','zipcode']

class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']