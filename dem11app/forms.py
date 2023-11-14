
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'ph_no', 'address']

class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MedicineForm(forms.ModelForm):
    class Meta:
        model=medicines
        fields=['name','dosage','disease','quantity','expirydate','contents','manufacturer']


class AidsForm(forms.ModelForm):
    class Meta:
        model=OtherAids
        fields=['name','age','rate','manufacturer']


