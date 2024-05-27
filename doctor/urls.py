from django.urls import  path
from . import views

urlpatterns = [
    path('', views.doctor_home, name='doctor_home'),
    path('appointments/', views.appointment, name='appointments'),
    path('patients-info/', views.patients, name='patients'),
    path('encounter/<int:appointmentid>/<int:userid>/', views.submit_form, name='encounter'),
    path('patients-history/<int:patient>/', views.pattient_history, name='patients_history'),
    path('encounter/api/diagnoses/', views.get_diagnoses, name='get_diagnoses'),
    path('encounter/api/symptoms/', views.get_symptoms, name='get_symptoms'),
    path('encounter/api/prescriptions/', views.get_prescriptions, name='get_prescriptions'),
    path('patient-assessment/<int:patientid>', views.patient_assessment, name='patient_assessment'),
    path('finish-appoinment/<int:appointmentid>', views.finish_appointment, name='finish_appointment'),
]
