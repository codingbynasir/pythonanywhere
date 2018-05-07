from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import patient, delete_account, shipping


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class patientForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = [
            "birth_date",
            "weight",
            "height",
            "smoker",
            "sex",
            "phone",
            'image'
        ]

class ShippingForm(forms.ModelForm):
    class Meta:
        model=shipping
        fields=[
            "city",
            "area",
            "address",
            "alternative_mobile_no",
        ]

class deleteForm(forms.ModelForm):
    class Meta:
        model = delete_account
        fields = ['reason']
