from datetime import datetime
from django.shortcuts import redirect, render
from accounts.models import Account
from doctor.models import AvailabilityTime, Department, Doctor ,DoctorAvailability
from patient.models import Appointment, Patient
from django.contrib import messages
from doctor.froms import AvailabilityTimeForm

def manager_home(request):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.filter(created_at__startswith=current_time[:10]).count()
    total_patients_added_today = Account.objects.filter(date_joined__startswith=current_time[:10], type='patient').count()
    total_doctors = Account.objects.filter(type='doctor').count()

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_patients_added_today': total_patients_added_today,
        'total_doctors': total_doctors,
    }
    return render(request, 'manager/index.html', context)

def doctor_operations(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        doctor.department = department
        doctor.save()
        messages.success(request, 'Doctor assigned to department successfully')
        return redirect('doctor_operations')
    else:
        context={
            'doctors': Doctor.objects.all(),
            'departments': Department.objects.all(),
        }
        return render(request, 'manager/doctor-operations.html', context)


def assign_department(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        print(doctor_id, department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        doctor.department = department
        doctor.save()
    return render(request, 'manager/doctor-operations.html')

def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully')
    return render(request, 'manager/doctor-operations.html')

def doctor_add(request):
    return render(request, 'manager/doctor-add.html')

def doctor_time_operations(request):
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
                DoctorAvailability.objects.create(doctor=doctor, availability=time)
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
    
def delete_doctor_time(request, drtime_id):
    drtime = DoctorAvailability.objects.get(id=drtime_id)
    drtime.delete()
    messages.success(request, 'Doctor time deleted successfully')
    return redirect('doctor_time_operations')

def hospital_time_operations(request):
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

def delete_available_time(request, time_id):
    time = AvailabilityTime.objects.get(id=time_id)
    time.delete()
    messages.success(request, 'Time deleted successfully')
    return redirect('hospital_time_operations')
