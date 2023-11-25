
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
# class MedicineForm(forms.ModelForm):
#     class Meta:
#         model=medicines
#         fields=['name','dosage','disease','quantity','expirydate','contents','manufacturer']
#     disease_choices=[
#         ('','select a disease'),
#         ('other','Other'),
#     ]
#     disease = forms.ModelChoiceField(
#         queryset=medicines.objects.values_list('disease', flat=True).distinct(),
#         empty_label="Select a disease",
#         to_field_name="disease",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
class MedicineForm(forms.ModelForm):
    class Meta:
        model = medicines
        fields = ['name', 'dosage', 'disease', 'quantity', 'expirydate', 'contents', 'manufacturer']

    def __init__(self, *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)

        # Add 'Other' as a choice in the disease field
        self.fields['disease'].choices = self.get_disease_choices()

    def get_disease_choices(self):
        # Get distinct diseases from the model and add 'Other' as a choice
        diseases = medicines.objects.values_list('disease', flat=True).distinct()
        choices = [(d, d) for d in diseases]
        choices.append(('Other', 'Other'))
        return choices
    disease = forms.ModelChoiceField(
        queryset=(medicines.objects.values_list('disease', flat=True).distinct()),
        empty_label="Select a disease",
        to_field_name="disease",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

# class MedicineForm(forms.ModelForm):
#     class Meta:
#         model = medicines
#         fields = ['name', 'dosage', 'disease', 'quantity', 'expirydate', 'contents', 'manufacturer']

#     disease = forms.ModelChoiceField(
#         queryset=medicines.objects.none(),  # Start with an empty queryset
#         empty_label="Select a disease",
#         to_field_name="disease",
#         widget=forms.Select(attrs={'class': 'form-control'}),
#     )

#     def __init__(self, *args, **kwargs):
#         super(MedicineForm, self).__init__(*args, **kwargs)

#         # Add 'Other' as a choice in the disease field
#         self.set_disease_choices()

#     def set_disease_choices(self):
#         # Get distinct diseases from the model and add 'Other' as a choice
#         diseases = medicines.objects.values_list('disease', flat=True).distinct()
#         choices = [(d, d) for d in diseases]
#         choices.append(('Other', 'Other'))

#         # Set the choices dynamically for the disease field
#         self.fields['disease'].widget.choices = choices
#     def clean(self):
#         cleaned_data = super().clean()
#         disease = cleaned_data.get('disease')
#         other_disease = cleaned_data.get('other_disease')

#         if disease == 'Other':
#             # If 'Other' is selected, use the value from the 'other_disease' field
#             cleaned_data['disease'] = other_disease

#         return cleaned_data

class AidsForm(forms.ModelForm):
    class Meta:
        model=OtherAids
        fields=['name','age','rate','manufacturer','current_photo']

    

# class Req_med_Form(forms.ModelForm):
#     class Meta:
#         model=req_med
#         fields=['medicine','quantity','disease','prescription_photo']
#     medicine = forms.ModelChoiceField(
#         queryset=medicines.objects.all(),
#         empty_label="Select a Medicine",
#         to_field_name="name",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
    
#     disease = forms.ModelChoiceField(
#         queryset=medicines.objects.values_list('disease', flat=True).distinct(),
#         empty_label="Select a Disease",
#         to_field_name="disease",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

class Req_med_Form(forms.ModelForm):
    class Meta:
        model = req_med
        fields = ['medicine', 'quantity', 'disease', 'prescription_photo']

    medicine = forms.ModelChoiceField(
        queryset=medicines.objects.all(),
        empty_label="Select a Medicine",
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    disease = forms.ModelChoiceField(
        queryset=medicines.objects.values_list('disease', flat=True).distinct(),
        empty_label="Select a Disease",
        to_field_name="disease",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'updateMedicineList()'})
    )

    def __init__(self, *args, **kwargs):
        super(Req_med_Form, self).__init__(*args, **kwargs)
        # Set a default empty queryset for the medicine field
        self.fields['medicine'].queryset = medicines.objects.none()

        # If the instance exists (editing an existing req_med), set initial values for medicine and disease
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['medicine'].initial = instance.medicine
            self.fields['disease'].initial = instance.disease

    class Media:
        js = ('js/req_med_form.js',)
