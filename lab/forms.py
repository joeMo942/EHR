# forms.py
from django import forms
from patient.models import TestResultField

class TestResultFieldForm(forms.ModelForm):
    class Meta:
        model = TestResultField
        fields = ['testfiled', 'result', 'isupnormal']
        widgets = {
            'testfiled': forms.HiddenInput(),  # Hide the testfiled field in the form
        }
