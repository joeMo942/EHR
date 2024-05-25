from django.contrib import admin

# admin.py
from django.contrib import admin
from .models import Nurse, InitialAssessment

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

@admin.register(InitialAssessment)
class InitialAssessmentAdmin(admin.ModelAdmin):
    list_display = ('medical', 'temperature', 'weight', 'blood_pressure', 'height', 'reason_of_visit')
    search_fields = ('medical__user__email', 'medical__user__first_name', 'medical__user__last_name')
    list_filter = ('medical', 'reason_of_visit')

