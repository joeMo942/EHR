from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, Allergies, CurrentMedication, Appointment
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, Allergies, CurrentMedication
from doctor.models import Department , Doctor, DoctorAvailability
from django.http import JsonResponse



@login_required
@csrf_protect
def save_medical_history(request):
    user = request.user
    patient= get_object_or_404(Patient, user=user)


    if request.method == 'POST':
        # Delete existing medical history for this patient if it exists
        MedicalHis.objects.filter(patient_no=patient).delete()

        # Save the new medical history
        medical_history = MedicalHis.objects.create(
            patient_no=patient,
            alcohol='Alcohol' in request.POST.getlist('conditions'),
            smoking='Smoking' in request.POST.getlist('conditions'),
            high_blood_pressure='HighBloodPressure' in request.POST.getlist('conditions'),
            diabetes='Diabetes' in request.POST.getlist('conditions'),
            high_colest='HighCholesterol' in request.POST.getlist('conditions')
        )

        # Save vaccinations
        vaccinations = request.POST.getlist('vaccinations')
        for vaccination in vaccinations:
            Vaccination.objects.get_or_create(vaccination_name=vaccination, history_no=medical_history)

        # Save diseases
        diseases = request.POST.getlist('diseases')
        for disease in diseases:
            Disease.objects.get_or_create(disease_name=disease, history_no=medical_history)

        # Save illnesses
        illnesses = request.POST.getlist('illnesses')
        for illness in illnesses:
            Illness.objects.get_or_create(illness_name=illness, history_no=medical_history)

        # Save previous surgeries
        prev_surgeries = request.POST.getlist('prevSurgeries')
        for prev_surgery in prev_surgeries:
            PrevSurgery.objects.get_or_create(prev_surgery_name=prev_surgery, history_no=medical_history)

        # Save medication allergies, filtering out any blank entries
        medication_allergies = [allergy for allergy in request.POST.getlist('medicationAllergies') if allergy.strip()]
        for allergy in medication_allergies:
            Allergies.objects.get_or_create(name=allergy, category='medication', history_no=medical_history)

        # Save food allergies, filtering out any blank entries
        food_allergies = [allergy for allergy in request.POST.getlist('foodAllergies') if allergy.strip()]
        for allergy in food_allergies:
            Allergies.objects.get_or_create(name=allergy, category='food', history_no=medical_history)

        # Save current medications
        medications_names = request.POST.getlist('medications[name]')
        medications_dosages = request.POST.getlist('medications[dosage]')
        medications_durations = request.POST.getlist('medications[duration]')

        for name, dosage, duration in zip(medications_names, medications_dosages, medications_durations):
            if name.strip():  # Ensure medication name is not blank
                CurrentMedication.objects.get_or_create(
                    name=name,
                    dosage=dosage,
                    duration=duration,
                    history_no=medical_history
                )

        messages.success(request, "Your medical history has been updated successfully")
        return redirect('medical_his')

    else:
        # Retrieve the existing medical history for this patient
        try:
            medical_history = MedicalHis.objects.get(patient_no=patient)
            vaccinations = [v.vaccination_name for v in Vaccination.objects.filter(history_no=medical_history)]
            diseases = [d.disease_name for d in Disease.objects.filter(history_no=medical_history)]
            illnesses = [i.illness_name for i in Illness.objects.filter(history_no=medical_history)]
            prev_surgeries = PrevSurgery.objects.filter(history_no=medical_history)
            medication_allergies = Allergies.objects.filter(history_no=medical_history, category='medication')
            food_allergies = Allergies.objects.filter(history_no=medical_history, category='food')
            current_medications = CurrentMedication.objects.filter(history_no=medical_history)
        except MedicalHis.DoesNotExist:
            medical_history = None
            vaccinations = []
            diseases = []
            illnesses = []
            prev_surgeries = []
            medication_allergies = []
            food_allergies = []
            current_medications = []

        context = {
            'user': user,
            'medical_history': medical_history,
            'vaccinations': vaccinations,
            'diseases': diseases,
            'illnesses': illnesses,
            'prev_surgeries': prev_surgeries,
            'medication_allergies': medication_allergies,
            'food_allergies': food_allergies,
            'current_medications': current_medications,
        }
        return render(request, 'patient/history.html', context)

@login_required
def appointment(request):
    user = request.user
    patient= get_object_or_404(Patient, user=user)
    print(user)
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        availability_id = request.POST.get('availableAppointments')
        print(availability_id)
        patient = patient
        doctor = get_object_or_404(Doctor, id=doctor_id)
        availability = get_object_or_404(DoctorAvailability, id=availability_id)
        department = doctor.department
        price = department.fees

        existing_appointment = Appointment.objects.filter(
            patient_no=patient,
            doctor=doctor,
            availability_time=availability
        ).exists()

        if existing_appointment:
            messages.error(request, "You already have an appointment at this time.")
            return redirect('appointment')
        else:
            appointment = Appointment.objects.create(
                patient_no=patient,
                doctor=doctor,
                department=department,
                availability_time=availability,
                price=price,
                status='Pending'
            )
            
            messages.success(request, "Your appointment has been scheduled successfully")
            return redirect('appointment')
        
    departments = Department.objects.all()
    print(departments)
    return render(request, 'patient/appointment.html',{'departments': departments})

def patient_home(request):
    return render(request, 'patient/index.html')


def get_doctors_by_department(request):
    department_id = request.GET.get('department_id')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id).values('id', 'user__first_name', 'user__last_name')
        return JsonResponse({'doctors': list(doctors)})
    return JsonResponse({'doctors': []})

def get_availability_by_doctor(request):
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        availabilities = DoctorAvailability.objects.filter(doctor_id=doctor_id).values('id', 'availability__day_of_week', 'availability__start_time', 'availability__end_time')
        doctor = Doctor.objects.get(id=doctor_id)
        department_price = doctor.department.fees
        return JsonResponse({'availabilities': list(availabilities), 'price': department_price})
    return JsonResponse({'availabilities': [], 'price': 0})


    
@login_required
def booked_appointment(request):
    user=request.user
    patient= get_object_or_404(Patient, user=user)
    appointments = Appointment.objects.filter(patient_no=patient)
    return render(request, 'patient/booked-appointment.html', {'appointments': appointments})

def test_results(request):
    return render(request, 'patient/test-results.html')

