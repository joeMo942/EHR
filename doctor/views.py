from django.shortcuts import render

def doctor_home(request):
    return render(request, 'doctor/index.html')

def appointment(request):
    return render(request, 'doctor/appointments.html')

def patients(request):
    return render(request, 'doctor/patient-info.html')

def encounter(request):
    return render(request, 'doctor/encounter.html')