from django.urls import  path
from . import views

urlpatterns = [
    path('', views.doctor_home, name='doctor_home'),
    path('appointments/', views.appointment, name='appointments'),
    path('patients-info/', views.patients, name='patients'),
    path('encounter/', views.encounter, name='encounter'),
]
