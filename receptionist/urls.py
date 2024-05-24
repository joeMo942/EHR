from django.urls import  path
from . import views

urlpatterns = [
    path('', views.receptionist_home, name='receptionist_home'),
    path('current-appointments/', views.current_appointments, name='current_appointments'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('api/doctors/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('get-full-name/', views.get_full_name, name='get_full_name'),
    path('patients-bills/', views.patients_bills, name='patients_bills'),
]
