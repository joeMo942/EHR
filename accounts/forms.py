from django import forms
from .models import Account


import re
from django.contrib.auth.password_validation import validate_password


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'Enter Birth Date',
        'class': 'form-control',
        'type': 'date'
    }))

    contact_no = forms.RegexField(
        regex=r'^\+\d{1,3}\d{7,15}$',
        error_messages={
            'invalid': 'Enter a valid phone number. E.g. +123456789'
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Contact Number with Country Code',
            'class': 'form-control',
        })
    )

    ssn = forms.RegexField(
        regex=r'^\d{14}$',
        error_messages={
            'invalid': 'Enter a valid SSN. It should be exactly 14 digits.'
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter SSN',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'type', 'ssn', 'contact_no', 'birth_date', 'gender']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Using Django's built-in password validators
        return password

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'