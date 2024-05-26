from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_home, name='manager_home'),
    path('doctor-operations/', views.doctor_operations, name='doctor_operations'),
    path('doctor-add/', views.doctor_add, name='doctor_add'),
]