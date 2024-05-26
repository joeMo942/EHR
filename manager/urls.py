from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_home, name='manager_home'),
    path('doctor-operations/', views.doctor_operations, name='doctor_operations'),
    path('doctor-add/', views.doctor_add, name='doctor_add'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('assign-department/', views.assign_department, name='assign_department'),
]