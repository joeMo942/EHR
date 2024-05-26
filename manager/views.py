from datetime import datetime
from django.shortcuts import render
from accounts.models import Account
from patient.models import Appointment, Patient

def manager_home(request):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.filter(created_at__startswith=current_time[:10]).count()
    total_patients_added_today = Account.objects.filter(date_joined__startswith=current_time[:10], type='patient').count()
    total_doctors = Account.objects.filter(type='doctor').count()

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_patients_added_today': total_patients_added_today,
        'total_doctors': total_doctors,
    }
    return render(request, 'manager/index.html', context)

def doctor_operations(request):
    return render(request, 'manager/doctor-operations.html')

def doctor_add(request):
    return render(request, 'manager/doctor-add.html')

def doctor_time_operations(request):
    return render(request, 'manager/doctor-time-operations.html')

def hospital_time_operations(request):
    return render(request, 'manager/hospital-time-operations.html')
