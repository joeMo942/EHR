# forms.py
from django import forms
from .models import InitialAssessment

class InitialAssessmentForm(forms.ModelForm):
    class Meta:
        model = InitialAssessment
        fields = ['temperature', 'weight', 'blood_pressure', 'height', 'reason_of_visit', 'notes']
