from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_no', 'department', 'doctor', 'availability_time', 'status', 'price']
