from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control',
    }))

    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'Enter Birth Date',
        'class': 'form-control',
        'type': 'date'
    }))
    class Meta:
        model = Account
        fields= ['first_name', 'last_name', 'email', 'password','type', 'ssn', 'contact_no', 'birth_date', 'gender']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            

    def __init__(self,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['ssn'].widget.attrs['placeholder'] = 'Enter SSN'
        self.fields['contact_no'].widget.attrs['placeholder'] = 'Enter Contact Number'

        for filed in self.fields:
            self.fields[filed].widget.attrs['class'] = 'form-control form-control-lg'
