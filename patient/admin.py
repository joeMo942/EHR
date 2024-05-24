from django.contrib import admin

# Register your models here.

from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, Allergies, CurrentMedication, Appointment
from .models import Medicationlu, Diagnosislu, Symptomslu, Diagnosislu, Encounters

admin.site.register(Medicationlu)
admin.site.register(Diagnosislu)
admin.site.register(Symptomslu)
admin.site.register(Encounters)
admin.site.register(Patient)
admin.site.register(MedicalHis)
admin.site.register(Vaccination)
admin.site.register(Disease)
admin.site.register(Illness)
admin.site.register(PrevSurgery)
admin.site.register(Allergies)
admin.site.register(CurrentMedication)
admin.site.register(Appointment)