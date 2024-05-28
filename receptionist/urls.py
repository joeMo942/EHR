from django.urls import  path
from . import views

urlpatterns = [
    path('', views.receptionist_home, name='receptionist_home'),
    path('current-appointments/', views.current_appointments, name='current_appointments'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('api/doctors/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('get-full-name/', views.get_full_name, name='get_full_name'),
    path('patients-bills/', views.patients_bills, name='patients_bills'),
    path('update-appointment-status/', views.update_appointment_status, name='update_appointment_status'),
    path('create-appointment/', views.book_appointment, name='create_appointment'),
    path('patients-bills/<int:appointment>', views.patients_bills_confirm, name='patients_bills_confirm'),
    path('cancel-appointment/<int:appointment>', views.cancel_appointment, name='cancel_appointment')

]
