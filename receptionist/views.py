from django.http import JsonResponse
from django.shortcuts import render

from doctor.models import Department, Doctor, Account

def receptionist_home(request):
    return render(request, 'receptionist/index.html')

def current_appointments(request):
    return render(request, 'receptionist/current-appointments.html')

def book_appointment(request):
    departments = Department.objects.all()
    context={
        'departments':departments
    }
    return render(request, 'receptionist/book-appointment.html',context)

def get_doctors_by_department(request):
    department_id = request.GET.get('department_id')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id).values('id', 'user__first_name', 'user__last_name')
        return JsonResponse({'doctors': list(doctors)})
    return JsonResponse({'doctors': []})

def get_full_name(request):
    ssn = request.GET.get('ssn', None)
    data = {
        'full_name': 'Not found'
    }
    if ssn:
        try:
            account = Account.objects.get(ssn=ssn)
            data['full_name'] = f"{account.first_name} {account.last_name}"
        except Account.DoesNotExist:
            data['full_name'] = 'Not found'
    return JsonResponse(data)

def patients_bills(request):
    return render(request, 'receptionist/patients-bills.html')