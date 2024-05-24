from django.urls import  path
from . import views

urlpatterns = [
    path('medical_his/', views.save_medical_history, name='medical_his'),
    path('', views.patient_home, name='patient_home'),
    path('appointment/', views.appointment, name='appointment'),

]
