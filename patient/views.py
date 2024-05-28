from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import Http404, HttpResponse
from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, CurrentMedication, Appointment,Allergies,Test,Encounters
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# from .models import Patient, MedicalHis, Vaccination, Disease, Illness, PrevSurgery, Allergies, CurrentMedication
from doctor.models import Department , Doctor, DoctorAvailability
from django.http import JsonResponse
from nurse.models import Nurse, InitialAssessment
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage

def profile(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        print(current_password)
        print(user)
        
        # Authenticate the user with the current password
        user = authenticate(email=user, password=current_password)
        print(user)
        if user is not None:
            # If the password is correct, process the form data and the image upload
            if 'img[]' in request.FILES:
                image = request.FILES['img[]']
                patient.image = image
                patient.save()
            else:
                uploaded_file_url = None

            # Process form data
            profile_data = {
                'ssn': request.POST.get('ssn'),
                'medid': request.POST.get('medid'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'gender': request.POST.get('gender'),
                'dob': request.POST.get('dob'),
                'category': request.POST.get('category'),
                'mobile_number': request.POST.get('mobile_number'),
                'email': request.POST.get('email'),
                'new_password': request.POST.get('new_password')
            }

            # Update user profile (assuming you have a Profile model or similar)
            # Example:
            user.ssn = profile_data['ssn']
            user.first_name = profile_data['first_name']
            user.last_name = profile_data['last_name']
            user.gender = profile_data['gender']
            # user.birth_date = profile_data['dob']
            user.contact_no = profile_data['mobile_number']
            
            # Update password if provided
            new_password = profile_data['new_password']
            if new_password:
                user.set_password(new_password)
            
            user.save()
            patient.save()
            
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')  # Replace 'profile' with your URL name for the profile page

        else:
            # If the password is incorrect, show an error message
            messages.error(request, 'Current password is incorrect')

    context = {
       'user': user,
        'patient': patient  # Default profile image URL
    }
    return render(request, 'patient/profile.html', context)


@login_required
@csrf_protect
def save_medical_history(request):
    user = request.user
    if user.type != 'patient':
        raise Http404
        
    patient = get_object_or_404(Patient, user=user)


    if request.method == 'POST':
        MedicalHis.objects.filter(patient_no=patient).delete()

        medical_history = MedicalHis.objects.create(
            patient_no=patient,
            alcohol='Alcohol' in request.POST.getlist('conditions'),
            smoking='Smoking' in request.POST.getlist('conditions'),
            high_blood_pressure='HighBloodPressure' in request.POST.getlist('conditions'),
            diabetes='Diabetes' in request.POST.getlist('conditions'),
            high_colest='HighCholesterol' in request.POST.getlist('conditions'),
            additional_notes=request.POST.get('additional_notes')
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
        patient.is_active = True
        patient.save()
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
    if user.type != 'patient':
        raise Http404
    patient= get_object_or_404(Patient, user=user)
    if patient.is_active == False:
        messages.error(request, "Your account can't book appointment till you finish your history.finish it")
        return redirect('medical_his')
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

@login_required
def patient_home(request):
    user=request.user
    if user.type not in ['patient','receptionist'] :
        raise Http404
    
    else:
        patient = get_object_or_404(Patient, user=request.user)
        assessments = InitialAssessment.objects.filter(patient=patient).values('blood_pressure', 'temperature', 'weight')
        
        # Assuming there's only one initial assessment per patient, we can fetch the first one
        assessment = assessments.first() if assessments else None
        
        context = {
            'blood_pressure': assessment['blood_pressure'] if assessment else None,
            'temperature': assessment['temperature'] if assessment else None,
            'weight': assessment['weight'] if assessment else None,
        }
        return render(request, 'patient/index.html', context)


@login_required
def get_doctors_by_department(request):
    user=request.user
    if user.type != 'patient':
        raise Http404
    department_id = request.GET.get('department_id')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id).values('id', 'user__first_name', 'user__last_name')
        return JsonResponse({'doctors': list(doctors)})
    return JsonResponse({'doctors': []})
@login_required
def get_availability_by_doctor(request):
    user=request.user
    if user.type != 'patient':
        raise Http404
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        today = date.today()
        next_three_availabilities = (DoctorAvailability.objects
                                 .filter(doctor_id=doctor_id, date__gte=today)
                                 .order_by('date')[:6]
                                 .values('id', 'availability__day_of_week', 'availability__start_time', 'availability__end_time', 'date'))
        
        doctor = Doctor.objects.get(id=doctor_id)
        department_price = doctor.department.fees
        return JsonResponse({'availabilities': list(next_three_availabilities), 'price': department_price})
    return JsonResponse({'availabilities': [], 'price': 0})


    
@login_required
def booked_appointment(request):
    user=request.user
    if user.type != 'patient':
        raise Http404
    patient= get_object_or_404(Patient, user=user)
    appointments = Appointment.objects.filter(patient_no=patient)
    return render(request, 'patient/booked-appointment.html', {'appointments': appointments})

@login_required
def test_results(request):
    user=request.user
    if user.type != 'patient':
        raise Http404
    tests=Test.objects.filter(patient__user=user)
    context={
        'tests':tests
    }
    return render(request, 'patient/test-results.html', context)

@login_required
def encounter(request, appointment_id):
    user=request.user
    if user.type != 'patient':
        raise Http404
    appointment = get_object_or_404(Appointment, id=appointment_id)
    encounters = get_object_or_404(Encounters,appointment=appointment)
    symptoms =encounters.symptoms.all()
    diagnosis = encounters.diagnosis.all()
    prescriptions = encounters.prescription.all()
    tests = encounters.tests.all()
    notes = encounters.notes
    context={
        'appointment':appointment,
        'symptoms':symptoms,
        'diagnosis':diagnosis,
        'prescriptions':prescriptions,
        'tests':tests,
        'notes':notes
    }
    return render(request, 'patient/encounter.html', context)

@login_required
def request_delete(request, appointment_id):
    user=request.user
    if user.type != 'patient':
        raise Http404
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status='cancel_request'
    appointment.save()
    messages.success(request, "Your cancellation request has been sent successfully")
    return redirect('booked_appointment')