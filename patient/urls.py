from django.urls import  path
from . import views


urlpatterns = [
    path('medical_his/', views.save_medical_history, name='medical_his'),
    path('', views.patient_home, name='patient_home'),
    path('appointment/', views.appointment, name='appointment'),
    path('api/doctors/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('api/availability/', views.get_availability_by_doctor, name='get_availability_by_doctor'),

    path('booked-appointment/', views.booked_appointment, name='booked_appointment'),
    path('test-results/', views.test_results, name='test_results'),
]
