from django.contrib import admin

# Register your models here.

from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, Allergies, CurrentMedication

admin.site.register(Patient)
admin.site.register(MedicalHis)
admin.site.register(Vaccination)
admin.site.register(Disease)
admin.site.register(Illness)
admin.site.register(PrevSurgery)
admin.site.register(Allergies)
admin.site.register(CurrentMedication)