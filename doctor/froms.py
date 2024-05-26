from django import forms
from .models import AvailabilityTime

class AvailabilityTimeForm(forms.ModelForm):
    class Meta:
        model = AvailabilityTime
        fields = ['start_time', 'end_time', 'day_of_week']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
        }
