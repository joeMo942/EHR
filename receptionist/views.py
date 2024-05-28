from datetime import date, datetime
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from doctor.models import Department, Doctor, DoctorAvailability
from accounts.models import Account
from patient.models import Patient, Appointment, Test
from django.core.serializers import serialize
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def receptionist_home(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")

    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.filter(created_at__startswith=current_time[:10]).count()
    total_patients_added_today = Account.objects.filter(date_joined__startswith=current_time[:10]).count()
    total_lab_results_done_today = Test.objects.filter(created_at__startswith=current_time[:10], status='Completed').count()

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_patients_added_today': total_patients_added_today,
        'total_lab_results_done_today': total_lab_results_done_today,
    }
    return render(request, 'receptionist/index.html', context)

@login_required
def current_appointments(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404

    # appointments = Appointment.objects.select_related('patient_no__user', 'doctor__user', 'availability_time__availability').all()
    appointments = Appointment.objects.filter(status__in=['Pending', 'Confirmed']).exclude(status='cancel_request').order_by('availability_time__date')
    cancel_appointments = Appointment.objects.filter(status='cancel_request').all()
    # Custom serialization to include related fields
    appointments_list = []
    for appointment in appointments:
        availability = appointment.availability_time.availability
        appointments_list.append({
            'id': appointment.id,
            'doctor_first_name': appointment.doctor.user.first_name,
            'doctor_last_name': appointment.doctor.user.last_name,
            'patient_first_name': appointment.patient_no.user.first_name,
            'patient_ssn': appointment.patient_no.user.ssn,  # Assuming the SSN is stored in the username field
            'availability_date': appointment.availability_time.date.isoformat(),  # Convert date to ISO format
            'start_time': availability.start_time.strftime('%H:%M:%S'),  # Convert time to string
            'end_time': availability.end_time.strftime('%H:%M:%S'),  # Convert time to string
            'day_of_week': availability.day_of_week,
            'status': appointment.status,
            
        })
    
    context = {
        'appointments_json': json.dumps(appointments_list),
        'cancel_appointments':cancel_appointments# Convert to JSON string
    }
    return render(request, 'receptionist/current-appointments.html', context)

@csrf_exempt  # Only use this for development; in production, properly handle CSRF tokens.
@require_POST
def update_appointment_status(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    appointment_id = request.POST.get('appointment_id')
    status = request.POST.get('status')

    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.availability_time.date < date.today():
            return JsonResponse({'success': False, 'error': 'Cannot change status of past appointments.'})
        
        appointment.status = status
        appointment.save()
        return JsonResponse({'success': True})
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Appointment does not exist.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def book_appointment(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    if request.method == 'POST':
        ssn = request.POST.get('ssn')
        try:
            patient = Patient.objects.get(user__ssn=ssn)
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
            return redirect('book_appointment')
        except Exception as e:
            messages.error(request, "An error occurred.")
            return redirect('book_appointment')
        patient = Patient.objects.get(user__ssn=ssn)
        doctor_id = request.POST.get('doctor')
        availability_id = request.POST.get('availableAppointments')
        print(availability_id)
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
            return redirect('book_appointment')
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
            return redirect('book_appointment')
    departments = Department.objects.all()
    context={
        'departments':departments
    }
    return render(request, 'receptionist/book-appointment.html',context)

@login_required
def get_doctors_by_department(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    department_id = request.GET.get('department_id')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id).values('id', 'user__first_name', 'user__last_name')
        return JsonResponse({'doctors': list(doctors)})
    return JsonResponse({'doctors': []})

@login_required
def get_full_name(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
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

@login_required
def patients_bills(request):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    appointments = Appointment.objects.filter(status='Not Paid')
    context = {
        'appointments': appointments
    }
    return render(request, 'receptionist/patients-bills.html', context)

@login_required
def patients_bills_confirm(request, appointment):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    appointments = get_object_or_404(Appointment, id=appointment)
    appointments.status = 'Paid'
    appointments.save()
    messages.success(request, "Payment has been confirmed")
    return redirect('patients_bills')

@login_required
def cancel_appointment(request, appointment):
    user=request.user
    if user.type!='receptionist':
        raise Http404
    appointments = get_object_or_404(Appointment, id=appointment)
    appointments.status='Declined'
    appointments.delete()
    # appointments.save()
    messages.success(request, "Appointment has been cancelled")
    return redirect('current_appointments')
