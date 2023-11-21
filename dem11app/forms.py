
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'ph_no', 'address']
        error_messages = {
            'username': {
                'required': 'Username is required.',
            },
            'password1': {
                'required': 'Password is required.',
            },
            'password2': {
                'required': 'Password confirmation is required.',
                'password_mismatch': 'The two passwords do not match.',
            },
        }

class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AdminForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Admin
        fields = ('username', 'password')
class MedicineForm(forms.ModelForm):
    class Meta:
        model=medicines
        fields=['name','dosage','disease','quantity','expirydate','contents','manufacturer']


class AidsForm(forms.ModelForm):
    class Meta:
        model=OtherAids
        fields=['name','age','rate','manufacturer','current_photo']

class Req_med_Form(forms.ModelForm):
    class Meta:
        model=req_med
        fields=['medicine','quantity','disease','prescription_photo']

