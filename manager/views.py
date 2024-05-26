from datetime import datetime
from django.shortcuts import redirect, render
from accounts.models import Account
from doctor.models import Department, Doctor
from patient.models import Appointment, Patient
from django.contrib import messages

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
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        doctor.department = department
        doctor.save()
        messages.success(request, 'Doctor assigned to department successfully')
        return redirect('doctor_operations')
    else:
        context={
            'doctors': Doctor.objects.all(),
            'departments': Department.objects.all(),
        }
        return render(request, 'manager/doctor-operations.html', context)


def assign_department(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        doctor.department = department
        doctor.save()
    return render(request, 'manager/doctor-operations.html')

def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    return render(request, 'manager/doctor-operations.html')

def doctor_add(request):
    return render(request, 'manager/doctor-add.html')

def doctor_time_operations(request):
    return render(request, 'manager/doctor-time-operations.html')

def hospital_time_operations(request):
    return render(request, 'manager/hospital-time-operations.html')
