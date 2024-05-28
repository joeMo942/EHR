from django.db import models
from accounts.models import Account
from doctor.models import Department, Doctor, DoctorAvailability



class Patient(models.Model):
    patient_no = models.IntegerField(primary_key=True,auto_created=True,blank=False) 
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='patient_images/', default='faces/default-profile.svg')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class MedicalHis(models.Model):
    patient_no = models.ForeignKey(Patient, on_delete=models.CASCADE,blank=False)
    alcohol = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    high_colest = models.BooleanField(default=False)
    additional_notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
       return f"{self.patient_no.user.first_name} {self.patient_no.user.last_name} medical history" 

class Vaccination(models.Model):
    vaccination_name = models.CharField(max_length=100)  
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)

    class Meta:
        unique_together  = (('vaccination_name', 'history_no'),)


class Disease(models.Model):
    disease_name = models.CharField(max_length=100)
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)  # The composite primary key (history_no, disease_name) found, that is not supported. The first column is selected.

    class Meta:
        unique_together  = (('history_no', 'disease_name'),)


class Illness(models.Model):
    illness_name = models.CharField(max_length=100)
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)  # The composite primary key (history_no, illness_name) found, that is not supported. The first column is selected.

    class Meta:
        unique_together = (('history_no', 'illness_name'),)


class PrevSurgery(models.Model):
    prev_surgery_name = models.CharField(max_length=100)
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)  # The composite primary key (history_no, prev_surgery_name) found, that is not supported. The first column is selected.

    class Meta:
        unique_together = (('history_no', 'prev_surgery_name'),)


class Allergies(models.Model):
    CATEGORY_CHOICES = [
        ('medication', 'Medication'),
        ('food', 'Food'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,blank=True, null=True)
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('history_no', 'name', 'category'),)

class CurrentMedication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    history_no = models.ForeignKey(MedicalHis, on_delete=models.CASCADE)  # The composite primary key (history_no, name) found, that is not supported. The first column is selected.

    class Meta:
        unique_together = (('history_no', 'name'),)

    
class Appointment(models.Model):
    Status_Choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Declined', 'Declined'),
        ('Not Paid', 'Not Paid'),
        ('Completed', 'Completed'),
        ('cancel_request', 'cancel_request'),
    ]
    patient_no = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    availability_time = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Status_Choices, default='Pending')
    price= models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('patient_no', 'availability_time'),)

    def __str__(self):
        return f"Appointment for {self.patient_no.user.first_name} with {self.doctor} at {self.availability_time}"

# lookups
class Symptomslu(models.Model):
    severity_cohices = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    symptomsname=models.CharField( max_length=100, unique=True )
    frequency=models.IntegerField(default=0)
    duration=models.CharField(max_length=50,blank=True, null=True)
    severity=models.CharField(max_length=50,choices=severity_cohices ,blank=True, null=True)
    def __str__(self):
        return self.symptomsname
    
class Diagnosislu(models.Model):
    diagnosisname=models.CharField(max_length=100, unique=True)
    icd_code=models.IntegerField(default=0 ,unique=True)
    description=models.CharField(max_length=500,blank=True, null=True)
    diagnositc_criteria=models.CharField(max_length=500,blank=True, null=True)
    treatment_option = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.diagnosisname
    
class Medicationlu(models.Model):
    medicationname = models.CharField(max_length=255, unique=True)
    genericname = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.IntegerField(default=0)

    strength = models.CharField(max_length=50, blank=True, null=True)
    avdosage = models.IntegerField(default=0, blank=True, null=True)
    routeofadministration = models.CharField(max_length=100, blank=True, null=True)
    package = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    lactation = models.IntegerField(blank=True, null=True)
    interaction = models.TextField(blank=True, null=True)
    pregnancy = models.BooleanField(blank=True, null=True)
    indication = models.TextField(blank=True, null=True)
    children = models.BooleanField(default=True, blank=True, null=True)
    effectondrive = models.TextField(blank=True, null=True)
    overdose = models.TextField(blank=True, null=True)
    sideeffects = models.TextField(blank=True, null=True)
    contraindications = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)
    storage = models.TextField(blank=True, null=True)
    pharmaceuticalform = models.TextField(blank=True, null=True)
    shelflife = models.CharField(max_length=50, blank=True, null=True)
    warningandprecautions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.medicationname

class Testfiled(models.Model):
    mesureunit=models.CharField(max_length=100, blank=True, null=True)
    shortname=models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=100, blank=True, null=True)
    refrance_range_up=models.IntegerField(default=0)
    refrance_range_down=models.IntegerField(default=0)

    class Meta:
        unique_together = (('name', 'mesureunit'),)

    def __str__(self):
        return self.name


class Testlu(models.Model):
    testname = models.CharField(max_length=100, unique=True)
    testfileds = models.ManyToManyField(Testfiled)
    type = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)

    class Meta:
        unique_together = (('testname', 'type'),)

    def __str__(self):
        return self.testname

# end lookups


class Prescription(models.Model):
    medication = models.ForeignKey(Medicationlu, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication.medicationname} {self.dosage} {self.frequency} {self.duration} prescription"



class Test(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    test = models.ForeignKey(Testlu, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100,choices=status_choices, default='Pending')   
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True, null=True)
    result = models.FileField(upload_to='test_results/', blank=True, null=True)
    result_notes = models.CharField(max_length=600, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.test.testname} test for {self.patient.user.first_name} {self.patient.user.last_name}"

class TestResultField(models.Model):
    testfiled = models.ForeignKey(Testfiled, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    isupnormal = models.BooleanField(default=False)
    test= models.ForeignKey(Test, on_delete=models.CASCADE ,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.test.testname} test result for {self.test.patient.user.first_name} {self.test.patient.user.last_name} filed {self.testfiled.name}"




class Encounters(models.Model):

    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptomslu, blank=True)
    diagnosis = models.ManyToManyField(Diagnosislu, blank=True)
    prescription = models.ManyToManyField(Prescription, blank=True)
    tests = models.ManyToManyField(Test, blank=True)
    appointment= models.OneToOneField(Appointment,on_delete=models.CASCADE)
    notes = models.CharField(max_length=600, blank=True, null=True)

    crearated_at = models.DateTimeField(auto_now_add=True)

    # e_time = models.TimeField(blank=True, null=True)
    # visit = models.ForeignKey('Visit', models.DO_NOTHING, blank=True, null=True)
    treatment_type = models.CharField(max_length=100, blank=True, null=True)
    # room_no = models.ForeignKey('Room', models.DO_NOTHING, db_column='room_no', blank=True, null=True)


    def __str__(self):
        return f"Encounter for {self.patient.user.first_name} with {self.doctor} "

    
