from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from doctor.models import Doctor
from patient.models import Patient,Appointment,Diagnosislu,Symptomslu,Medicationlu


def doctor_home(request):
    return render(request, 'doctor/index.html')


@login_required
def appointment(request):
    user=request.user
    doctor=get_object_or_404(Doctor,user=user)
    
    confirmed_appointments = Appointment.objects.filter(doctor=doctor, status='Confirmed')
    context = {'appointments': confirmed_appointments}
    return render(request, 'doctor/appointments.html', context)

def patients(request):
    return render(request, 'doctor/patient-info.html')


def encounter(request):
    print(request.GET)
    return render(request, 'doctor/encounter.html')


def get_diagnoses(request):
    if request.method == 'GET':
        diagnoses = Diagnosislu.objects.all().values('diagnosisname', 'icd_code')
        print(diagnoses)
        return JsonResponse({'diagnoses': list(diagnoses)})

def get_symptoms(request):
    if request.method == 'GET':
        symptoms = Symptomslu.objects.all().values_list('symptomsname', flat=True)
        print(symptoms)
        return JsonResponse({'symptoms': list(symptoms)})

def get_prescriptions(request):
    if request.method == 'GET':
        prescriptions = Medicationlu.objects.all().values_list('medicationname', flat=True)
        print(prescriptions)
        return JsonResponse({'prescriptions': list(prescriptions)})