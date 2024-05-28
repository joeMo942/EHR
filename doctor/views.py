from datetime import date
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from doctor.models import Doctor
from patient.models import Allergies, CurrentMedication, Disease, Encounters, Illness, MedicalHis, Patient,Appointment,Diagnosislu, PrevSurgery,Symptomslu,Medicationlu, Vaccination,Prescription,Testlu,Test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import date
from nurse.models import InitialAssessment


def doctor_home(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    total_appointments_for_doctor = Appointment.objects.filter(doctor__user=user).count()
    confirmed_appointments_for_doctor_today = Appointment.objects.filter(doctor__user=user, status='Confirmed', availability_time__date=date.today()).count()
    total_patients_for_doctor = Patient.objects.filter(appointment__doctor__user=user).count()
    context = {
        'total_appointments_for_doctor': total_appointments_for_doctor,
        'confirmed_appointments_for_doctor_today': confirmed_appointments_for_doctor_today,
        'total_patients_for_doctor': total_patients_for_doctor,
    }
    return render(request, 'doctor/index.html', context)


@login_required
def appointment(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return render(request, 'doctor/appointments ERORR.html')
    # doctor=get_object_or_404(Doctor,user=user)
    
    confirmed_appointments = Appointment.objects.filter(doctor=doctor, status='Confirmed')
    context = {'appointments': confirmed_appointments}
    return render(request, 'doctor/appointments.html', context)

@login_required
def patients(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    patients = Patient.objects.filter(appointment__doctor__user=user).distinct()
    context = {'patients': patients}
    return render(request, 'doctor/patient-info.html',context)


# def encounter(request):
#     print(request.GET)
#     return render(request, 'doctor/encounter.html')

@login_required
def get_diagnoses(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    
    if request.method == 'GET':
        diagnoses = Diagnosislu.objects.all().values('diagnosisname', 'icd_code')
        print(diagnoses)
        return JsonResponse({'diagnoses': list(diagnoses)})
@login_required
def get_symptoms(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    if request.method == 'GET':
        symptoms = Symptomslu.objects.all().values_list('symptomsname', flat=True)
        print(symptoms)
        return JsonResponse({'symptoms': list(symptoms)})
@login_required
def get_prescriptions(request):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    if request.method == 'GET':
        prescriptions = Medicationlu.objects.all().values_list('medicationname', flat=True)
        print(prescriptions)
        return JsonResponse({'prescriptions': list(prescriptions)})
    


@csrf_exempt
@login_required
def submit_form(request , appointmentid, userid):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    print(userid)
    patient= get_object_or_404(Patient, user=userid)
    appointment = get_object_or_404(Appointment, id=appointmentid)
    if request.method == 'POST':
        # Extract form data
        
        patient_id = patient.pk
        appointment_id = appointment.id

        # Extract Symptoms
        symptoms = request.POST.getlist('symptoms[]')
        print(symptoms)

        # Extract Diagnoses
        diagnosis_names = request.POST.getlist('diagnosisName[]')
        print(diagnosis_names)
        diagnosis_icds = request.POST.getlist('diagnosisICD[]')
        print(diagnosis_icds)

        # Extract Prescriptions
        prescription_names = request.POST.getlist('prescriptionName[]')
        prescription_dosages = request.POST.getlist('prescriptionDosage[]')
        prescription_frequencies = request.POST.getlist('prescriptionFrequency[]')
        prescription_durations = request.POST.getlist('prescriptionDuration[]')
        print(prescription_names)

        # Extract Test Requirement
        require_test = request.POST.get('requireTest')
        test_types = request.POST.getlist('testType[]')
        test_names = request.POST.getlist('testName[]')
        print(test_names)
        print(test_types)

        # Extract Notes
        notes = request.POST.get('notes')

        # Process and save data to the database
        # Fetch patient and appointment records
        patient = get_object_or_404(Patient, pk=patient_id)
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        # Create and save encounter record
        if Encounters.objects.filter(patient=patient, doctor=appointment.doctor, appointment=appointment).exists():
            Encounters.objects.filter(patient=patient, doctor=appointment.doctor, appointment=appointment).delete()
        
        encounter = Encounters.objects.get_or_create(
            patient=patient,
            doctor=appointment.doctor,
            appointment=appointment,
        )
        
        encounter=get_object_or_404(Encounters, patient=patient, doctor=appointment.doctor, appointment=appointment)
        # Save symptoms
        for symptom_name in symptoms:
            if symptom_name:
                try:
                    symptom = Symptomslu.objects.get(symptomsname=symptom_name)
                    encounter.symptoms.add(symptom)
                    print(encounter)
                except Symptomslu.DoesNotExist:
                    messages.error(request,f"Symptom '{symptom_name}' not found in the database.")
                    return redirect('encounter', appointmentid, userid)
                

        # Save diagnoses
        for name, icd in zip(diagnosis_names, diagnosis_icds):
            if name and icd:
                try:
                    diagnosis = Diagnosislu.objects.get(diagnosisname=name, icd_code=icd)
                    encounter.diagnosis.add(diagnosis)
                except Diagnosislu.DoesNotExist:
                    messages.error(request,f"Diagnosis '{name}' with ICD code '{icd}' not found in the database.")
                    return redirect('encounter', appointmentid, userid)


        # Save prescriptions
        for name, dosage, frequency, duration in zip(prescription_names, prescription_dosages, prescription_frequencies, prescription_durations):
            if name and dosage and frequency and duration:
                try:
                    medication = Medicationlu.objects.get(medicationname=name)
                except Medicationlu.DoesNotExist:
                    messages.error(f"Medication '{name}' not found in the database.")
                    return redirect('encounter', appointmentid, userid)

                if Prescription.objects.filter(medication=medication, dosage=dosage, frequency=frequency, duration=duration).exists() :
                    encounter.prescription.add(Prescription.objects.get(medication=medication, dosage=dosage, frequency=frequency, duration=duration))
                else:
                    prescription =Prescription.objects.create(medication=medication, dosage=dosage, frequency=frequency, duration=duration)
                    encounter.prescription.add(prescription)


        # Save tests if required
        if require_test == 'Yes':
            for test_type, test_name in zip(test_types, test_names):
                if test_type and test_name:
                    try:
                        test = Testlu.objects.get(testname=test_name, type=test_type)
                        test=Test.objects.create(test=test, patient=patient,appointment=appointment)
                        appointment.price += test.test.price
                        encounter.tests.add(test)
                    except Testlu.DoesNotExist:
                        messages.error(request,f"Test '{test_name}' of type '{test_type}' not found in the database.")
                        return redirect('encounter', appointmentid, userid)

        # Save additional notes
        if notes:
            encounter.notes = notes
        appointment.save()
        encounter.save()
        messages.success(request, 'Encounter saved successfully.')
        return redirect('encounter', appointmentid, userid)
    else:
        context = {
            'appointment': appointment,
            'patient': patient
        }
        return render(request, 'doctor/encounter.html' , context)
@login_required
def pattient_history(request, patient):
    user=request.user
    if user.type != 'doctor':
        raise Http404
    patient = get_object_or_404(Patient, pk=patient)
    context = {'patient': patient}

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
            'user': patient.user,
            'medical_history': medical_history,
            'vaccinations': vaccinations,
            'diseases': diseases,
            'illnesses': illnesses,
            'prev_surgeries': prev_surgeries,
            'medication_allergies': medication_allergies,
            'food_allergies': food_allergies,
            'current_medications': current_medications,
        }
    return render(request, 'doctor/patient-history.html', context)

def patient_assessment(request,patientid):
    patient=get_object_or_404(Patient,pk=patientid)
    initialassessment = InitialAssessment.objects.filter(patient=patient).order_by('date').last()

    context={
        'initialassessment':initialassessment,
        'patient':patient,
    }


    return render(request, 'doctor/patient-assessment.html',context)


def finish_appointment(request,appointmentid):
    appointment=get_object_or_404(Appointment,pk=appointmentid)
    appointment.status='Not Paid'
    appointment.save()
    messages.success(request, 'Appointment finished successfully.')
    return redirect('appointments')