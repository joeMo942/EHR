from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import InitialAssessment
from .forms import InitialAssessmentForm
from accounts.models import Account
from .models import Nurse
from patient.models import Patient
from django.contrib.auth.decorators import login_required


@login_required
def nurse_home(request):
    user = request.user
    if user.type != 'nurse':
        raise Http404
    return redirect('initial_assessment')


@login_required
def initial_assessment_view(request):
    user = request.user
    if user.type != 'nurse':
        raise Http404

    if request.method == 'POST':
        ssn=request.POST.get('ssn')
        temperature = request.POST.get('temperature')
        weight = request.POST.get('weight')
        blood_pressure = request.POST.get('bloodPressure')
        height = request.POST.get('height')
        reason_of_visit = request.POST.get('reasonOfVisit')
        notes = request.POST.get('notes')
        
            
        user=Account.objects.get(ssn=ssn)
        patient = Patient.objects.get(user=user)

        # Assuming the logged-in user is a nurse
        nurse = Nurse.objects.get(user=request.user)

        # Create InitialAssessment object manually
        initial_assessment = InitialAssessment.objects.create(
            temperature=temperature,
            weight=weight,
            blood_pressure=blood_pressure,
            height=height,
            reason_of_visit=reason_of_visit,
            notes=notes,
            medical=nurse,
            patient=patient
        )
        initial_assessment.save()
        print("Form is valid and data saved.")
        return redirect('initial_assessment')  # Redirect to a success page

        print("Form is not valid:", form.errors)
    else:
        print("t is not valid")
        form = InitialAssessmentForm()
    return render(request, 'nurse/initial-assessment.html', {'form': form})

def get_full_name(request):
    ssn = request.GET.get('ssn')
    try:
        patient = Account.objects.get(ssn=ssn)
        data = {'full_name': f"{patient.first_name} {patient.last_name}"}
    except Account.DoesNotExist:
        data = {'full_name': 'Not found'}
    return JsonResponse(data)
