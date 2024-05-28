from datetime import datetime
from django.http import Http404
from django.shortcuts import redirect, render
from accounts.models import Account
from doctor.models import AvailabilityTime, Department, Doctor ,DoctorAvailability
from patient.models import Appointment, Patient, Test
from django.contrib import messages
from doctor.froms import AvailabilityTimeForm
from django.contrib.auth.decorators import login_required



@login_required
def manager_home(request):
    user = request.user
    if user.type != 'admin':
        raise Http404

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.filter(created_at__startswith=current_time[:10]).count()
    total_patients_added_today = Account.objects.filter(date_joined__startswith=current_time[:10], type='patient').count()
    total_doctors = Account.objects.filter(type='doctor').count()
    total_lab_results_done = Test.objects.filter(status='Completed').count()

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_patients_added_today': total_patients_added_today,
        'total_doctors': total_doctors,
        'total_lab_results_done': total_lab_results_done,
    }
    return render(request, 'manager/index.html', context)

@login_required
def doctor_operations(request):
    user = request.user
    if user.type != 'admin':
        raise Http404
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Account.objects.get(pk=doctor_id)
        department = Department.objects.get(id=department_id)
        Doctor.objects.create(user=doctor, department=department)
        messages.success(request, 'Doctor assigned to department successfully')
        return redirect('doctor_operations')
    else:
        context={
            'unassigndoctors': Account.objects.filter(type='doctor'),
            'doctors': Doctor.objects.all(),
            'departments': Department.objects.all(),
        }
        return render(request, 'manager/doctor-operations.html', context)

@login_required
def assign_department(request):
    user = request.user
    if user.type != 'admin':
        raise Http404
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        doctor.department = department
        doctor.save()
    return render(request, 'manager/doctor-operations.html')

@login_required
def delete_doctor(request, doctor_id):
    user = request.user
    if user.type != 'admin':
        raise Http404
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully')
    return redirect('doctor_operations')


@login_required
def doctor_time_operations(request):
    user = request.user
    if user.type != 'admin':
        raise Http404
    if request.method == 'POST':
        doctor=request.POST.get('doctor')
        time=request.POST.get('time')
        if doctor and time:
            doctor=Doctor.objects.get(id=doctor)
            time=AvailabilityTime.objects.get(id=time)
            if DoctorAvailability.objects.filter(doctor=doctor, availability=time).exists():
                messages.error(request, 'Time already added to doctor')
                return redirect('doctor_time_operations')
            else:
                DoctorAvailability.objects.create(doctor=doctor, availability=time ,date=datetime.now())
                messages.success(request, 'Doctor time added successfully')
                return redirect('doctor_time_operations')
    else:
        doctors=Doctor.objects.all()
        availabilityTimes=AvailabilityTime.objects.all()
        context={
            'doctors':doctors,
            'availabilityTimes':availabilityTimes,
            'doctor_times': DoctorAvailability.objects.all(),
        }
        return render(request, 'manager/doctor-time-operations.html', context)

@login_required 
def delete_doctor_time(request, drtime_id):
    user = request.user
    if user.type != 'admin':
        raise Http404
    drtime = DoctorAvailability.objects.get(id=drtime_id)
    drtime.delete()
    messages.success(request, 'Doctor time deleted successfully')
    return redirect('doctor_time_operations')

@login_required
def hospital_time_operations(request):
    user = request.user
    if user.type != 'admin':
        raise Http404
    if request.method == 'POST':
        form = AvailabilityTimeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['start_time'] >= form.cleaned_data['end_time']:
                messages.error(request, 'Start time cannot be greater than or equal to end time')
                return redirect('hospital_time_operations')
            else:
                if AvailabilityTime.objects.filter(start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'] , day_of_week=form.cleaned_data['day_of_week']).exists():
                    messages.error(request, 'Time for this day already exists')
                    return redirect('hospital_time_operations')
                else:
                    form.save()
                    messages.success(request, 'Time added successfully')
            return redirect('hospital_time_operations')  # Redirect to a success page or another relevant page
    else:
        form = AvailabilityTimeForm()
        availabilityTime=AvailabilityTime.objects.all()
        context={
            'form':form,
            'availabilityTime':availabilityTime
        }
    return render(request, 'manager/hospital-time-operations.html' ,context)

@login_required
def delete_available_time(request, time_id):
    user = request.user
    if user.type != 'admin':
        raise Http404
    time = AvailabilityTime.objects.get(id=time_id)
    time.delete()
    messages.success(request, 'Time deleted successfully')
    return redirect('hospital_time_operations')
