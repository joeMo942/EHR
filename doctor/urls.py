from django.urls import  path
from . import views

urlpatterns = [
    path('', views.doctor_home, name='doctor_home'),
    path('appointments/', views.appointment, name='appointments'),
    path('patients-info/', views.patients, name='patients'),
    path('encounter/', views.encounter, name='encounter'),
    path('encounter/api/diagnoses/', views.get_diagnoses, name='get_diagnoses'),
    path('encounter/api/symptoms/', views.get_symptoms, name='get_symptoms'),
    path('encounter/api/prescriptions/', views.get_prescriptions, name='get_prescriptions'),
]
