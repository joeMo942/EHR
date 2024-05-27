# models.py
from django.db import models
from accounts.models import Account
from patient.models import Patient

class Nurse(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class InitialAssessment(models.Model):
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure = models.CharField(max_length=20)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reason_of_visit = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    medical = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
