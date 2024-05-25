from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from doctor.models import Doctor
from patient.models import Allergies, CurrentMedication, Disease, Encounters, Illness, MedicalHis, Note, Patient,Appointment,Diagnosislu, PrevSurgery,Symptomslu,Medicationlu, Test, Vaccination
from django.views.decorators.csrf import csrf_exempt


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


# def encounter(request):
#     print(request.GET)
#     return render(request, 'doctor/encounter.html')


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
    


@csrf_exempt
def submit_form(request , appointment, user):
    patient= get_object_or_404(Patient, user=user)
    appointment = get_object_or_404(Appointment, id=appointment)
    if request.method == 'POST':
        # Extract form data
        
        patient_id = request.POST.get('patientID')
        reason_for_visit = request.POST.get('reasonForVisit')
        appointment_id = appointment.id

        # Extract Symptoms
        symptoms = request.POST.getlist('symptoms[]')

        # Extract Diagnoses
        diagnosis_names = request.POST.getlist('diagnosisName[]')
        diagnosis_icds = request.POST.getlist('diagnosisICD[]')

        # Extract Prescriptions
        prescription_names = request.POST.getlist('prescriptionName[]')
        prescription_dosages = request.POST.getlist('prescriptionDosage[]')
        prescription_frequencies = request.POST.getlist('prescriptionFrequency[]')
        prescription_durations = request.POST.getlist('prescriptionDuration[]')

        # Extract Test Requirement
        require_test = request.POST.get('requireTest')
        test_types = request.POST.getlist('testType[]')
        test_names = request.POST.getlist('testName[]')

        # Extract Notes
        notes = request.POST.get('notes')

        # Process and save data to the database
        # Fetch patient and appointment records
        patient = get_object_or_404(Patient, pk=patient_id)
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        # Create and save encounter record
        encounter = Encounters.objects.create(
            patient=patient,
            doctor=appointment.doctor,
            appointment=appointment,
            notes=notes,
            treatment_type=reason_for_visit
        )

        # Save symptoms
        for symptom_name in symptoms:
            if symptom_name:
                symptom = get_object_or_404(Symptomslu, symptomsname=symptom_name)
                encounter.symptoms.add(symptom)

        # Save diagnoses
        for name, icd in zip(diagnosis_names, diagnosis_icds):
            if name and icd:
                diagnosis = get_object_or_404(Diagnosislu, diagnosisname=name, icd_code=icd)
                encounter.diagnosis.add(diagnosis)

        # Save prescriptions
        for name, dosage, frequency, duration in zip(prescription_names, prescription_dosages, prescription_frequencies, prescription_durations):
            if name and dosage and frequency and duration:
                medication = get_object_or_404(Medicationlu, medicationname=name)
                # Note: Here we should handle the actual logic of saving the prescription to the encounter
                # Since the original model doesn't include a prescription model, you might need to create one.

        # Save tests if required
        if require_test == 'Yes':
            for test_type, test_name in zip(test_types, test_names):
                if test_type and test_name:
                    Test.objects.create(patient=encounter, test_type=test_type, test_name=test_name)

        # Save additional notes
        if notes:
            Note.objects.create(patient=encounter, content=notes)

        return HttpResponse('Form submitted successfully.')
    else:
        context = {
            'appointment': appointment,
            'patient': patient
        }
        return render(request, 'doctor/encounter.html' , context)
    
def pattient_history(request, patient):
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