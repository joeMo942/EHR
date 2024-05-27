from django.urls import path
from . import views
from accounts.views import registerstaff


urlpatterns = [
    path('', views.manager_home, name='manager_home'),
    path('doctor-operations/', views.doctor_operations, name='doctor_operations'),
    path('doctor-time-operations/', views.doctor_time_operations, name='doctor_time_operations'),
    path('hospital-time-operations/', views.hospital_time_operations, name='hospital_time_operations'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('assign-department/', views.assign_department, name='assign_department'),
    path('delete-available-time/<int:time_id>/', views.delete_available_time, name='delete_available_time'),
    path('delete-doctor-time/<int:drtime_id>/', views.delete_doctor_time, name='delete_dcotor_time'),
    path('register-staff', registerstaff, name='register_staff')
]