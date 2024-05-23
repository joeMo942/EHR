# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Allergies(models.Model):
    name = models.CharField(max_length=100)
    history_no = models.OneToOneField('MedicalHis', models.DO_NOTHING, db_column='history_no', primary_key=True)  # The composite primary key (history_no, name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'allergies'
        unique_together = (('history_no', 'name'),)


class Appointment(models.Model):
    receptionist = models.OneToOneField('Receptionist', models.DO_NOTHING, primary_key=True)  # The composite primary key (receptionist_id, patient_no, appointment_id, availability_time_availability_id) found, that is not supported. The first column is selected.
    patient_no = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_no')
    appointment_id = models.IntegerField()
    department = models.CharField(max_length=50, blank=True, null=True)
    medical = models.ForeignKey('Doctor', models.DO_NOTHING, blank=True, null=True)
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    consult = models.ForeignKey('Encounters', models.DO_NOTHING, blank=True, null=True)
    availability_time_time = models.ForeignKey('AvailabilityTime', models.DO_NOTHING, db_column='availability_time_Time', to_field='a_time', blank=True, null=True)  # Field name made lowercase.
    availability_time_date = models.ForeignKey('AvailabilityTime', models.DO_NOTHING, db_column='availability_time_date', to_field='a_date', related_name='appointment_availability_time_date_set', blank=True, null=True)
    availability_time_availability = models.ForeignKey('AvailabilityTime', models.DO_NOTHING, related_name='appointment_availability_time_availability_set')
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'
        unique_together = (('receptionist', 'patient_no', 'appointment_id', 'availability_time_availability'),)


class AssignedTo(models.Model):
    patient_no = models.OneToOneField('Patient', models.DO_NOTHING, db_column='patient_no', primary_key=True)  # The composite primary key (patient_no, medical_id) found, that is not supported. The first column is selected.
    medical = models.ForeignKey('Nurse', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assigned_to'
        unique_together = (('patient_no', 'medical'),)


class AttendingDoctor(models.Model):
    dr = models.OneToOneField('Doctor', models.DO_NOTHING, primary_key=True)  # The composite primary key (dr_id, surgery_id) found, that is not supported. The first column is selected.
    surgery = models.ForeignKey('Surgery', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attending_doctor'
        unique_together = (('dr', 'surgery'),)


class AttendingNurse(models.Model):
    surgery = models.OneToOneField('Surgery', models.DO_NOTHING, primary_key=True)  # The composite primary key (surgery_id, medical_id) found, that is not supported. The first column is selected.
    medical = models.ForeignKey('Nurse', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attending_nurse'
        unique_together = (('surgery', 'medical'),)


class AvailabilityTime(models.Model):
    availability_id = models.IntegerField(primary_key=True)  # The composite primary key (availability_id, a_time, a_date) found, that is not supported. The first column is selected.
    a_time = models.TimeField()
    a_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'availability_time'
        unique_together = (('availability_id', 'a_time', 'a_date'),)


class Bill(models.Model):
    billno = models.IntegerField(primary_key=True)  # The composite primary key (billno, patient_no) found, that is not supported. The first column is selected.
    amount = models.IntegerField(blank=True, null=True)
    receptionist = models.ForeignKey('Receptionist', models.DO_NOTHING, blank=True, null=True)
    insurance = models.CharField(max_length=50, blank=True, null=True)
    patient_no = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_no')

    class Meta:
        managed = False
        db_table = 'bill'
        unique_together = (('billno', 'patient_no'),)


class Component(models.Model):
    testid = models.ForeignKey('MedTest', models.DO_NOTHING, db_column='TestID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    measurementunit = models.CharField(db_column='MeasurementUnit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=100, blank=True, null=True)  # Field name made lowercase.
    referencerange = models.CharField(db_column='ReferenceRange', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'component'


class CurrentMedication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    history_no = models.OneToOneField('MedicalHis', models.DO_NOTHING, db_column='history_no', primary_key=True)  # The composite primary key (history_no, name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'current_medication'
        unique_together = (('history_no', 'name'),)


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    medical_id = models.IntegerField(blank=True, null=True)
    fees = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class Diagnosis(models.Model):
    icd_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    treatment_option = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    diagnositc_criteria = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnosis'


class Disease(models.Model):
    disease_name = models.CharField(max_length=100)
    history_no = models.OneToOneField('MedicalHis', models.DO_NOTHING, db_column='history_no', primary_key=True)  # The composite primary key (history_no, disease_name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'disease'
        unique_together = (('history_no', 'disease_name'),)


class Doctor(models.Model):
    medical_id = models.IntegerField(primary_key=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    user = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class DrAvailabilityTime(models.Model):
    availability = models.ForeignKey(AvailabilityTime, models.DO_NOTHING)
    medical = models.OneToOneField(Doctor, models.DO_NOTHING, primary_key=True)  # The composite primary key (medical_id, availability_id) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'dr_availability_time'
        unique_together = (('medical', 'availability'),)


class Encounters(models.Model):
    consult_id = models.IntegerField(primary_key=True)
    icd_code = models.IntegerField(db_column='ICD_code', blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(max_length=600, blank=True, null=True)
    e_time = models.TimeField(blank=True, null=True)
    visit = models.ForeignKey('Visit', models.DO_NOTHING, blank=True, null=True)
    treatment_type = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.ForeignKey('Room', models.DO_NOTHING, db_column='room_no', blank=True, null=True)
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING, to_field='appointment_id', blank=True, null=True)
    referral_area = models.CharField(max_length=100, blank=True, null=True)
    referral_dep = models.CharField(max_length=100, blank=True, null=True)
    referral_details = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encounters'


class Illness(models.Model):
    illness_name = models.CharField(max_length=100)
    history_no = models.OneToOneField('MedicalHis', models.DO_NOTHING, db_column='history_no', primary_key=True)  # The composite primary key (history_no, illness_name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'illness'
        unique_together = (('history_no', 'illness_name'),)


class InitialAssessment(models.Model):
    assessment_id = models.IntegerField(primary_key=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reason_of_visit = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    medical = models.ForeignKey('Nurse', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'initial_assessment'


class LabSpecialist(models.Model):
    specialist_id = models.IntegerField(primary_key=True)  # The composite primary key (specialist_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey('Person', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lab_specialist'
        unique_together = (('specialist_id', 'user'),)


class MedTest(models.Model):
    testid = models.IntegerField(db_column='TestID', primary_key=True)  # Field name made lowercase. The composite primary key (TestID, specialist_id, consult_id) found, that is not supported. The first column is selected.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    specialist = models.ForeignKey(LabSpecialist, models.DO_NOTHING)
    consult = models.ForeignKey(Encounters, models.DO_NOTHING)
    status = models.CharField(max_length=50, blank=True, null=True)
    file_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'med_test'
        unique_together = (('testid', 'specialist', 'consult'),)


class MedicalHis(models.Model):
    history_no = models.AutoField(primary_key=True)
    patient_no = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_no', blank=True, null=True)
    alcohol = models.IntegerField(blank=True, null=True)
    smoking = models.IntegerField(blank=True, null=True)
    high_blood_pressure = models.IntegerField(blank=True, null=True)
    diabetes = models.IntegerField(blank=True, null=True)
    high_colest = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medical_his'


class Medication(models.Model):
    med_name = models.CharField(primary_key=True, max_length=100)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    med = models.ForeignKey('Medicationlu', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medication'


class Medicationlu(models.Model):
    medicationid = models.IntegerField(db_column='MedicationID', primary_key=True)  # Field name made lowercase.
    medicationname = models.CharField(db_column='MedicationName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genericname = models.CharField(db_column='GenericName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    strength = models.CharField(db_column='Strength', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=100, blank=True, null=True)  # Field name made lowercase.
    routeofadministration = models.CharField(db_column='RouteOfAdministration', max_length=100, blank=True, null=True)  # Field name made lowercase.
    package = models.CharField(db_column='Package', max_length=100, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lactation = models.IntegerField(db_column='Lactation', blank=True, null=True)  # Field name made lowercase.
    interaction = models.TextField(db_column='Interaction', blank=True, null=True)  # Field name made lowercase.
    pregnancy = models.IntegerField(db_column='Pregnancy', blank=True, null=True)  # Field name made lowercase.
    indication = models.TextField(db_column='Indication', blank=True, null=True)  # Field name made lowercase.
    children = models.IntegerField(db_column='Children', blank=True, null=True)  # Field name made lowercase.
    effectondrive = models.TextField(db_column='EffectOnDrive', blank=True, null=True)  # Field name made lowercase.
    overdose = models.TextField(db_column='Overdose', blank=True, null=True)  # Field name made lowercase.
    sideeffects = models.TextField(db_column='SideEffects', blank=True, null=True)  # Field name made lowercase.
    contraindications = models.TextField(db_column='Contraindications', blank=True, null=True)  # Field name made lowercase.
    composition = models.TextField(db_column='Composition', blank=True, null=True)  # Field name made lowercase.
    storage = models.TextField(db_column='Storage', blank=True, null=True)  # Field name made lowercase.
    pharmaceuticalform = models.TextField(db_column='PharmaceuticalForm', blank=True, null=True)  # Field name made lowercase.
    shelflife = models.CharField(db_column='ShelfLife', max_length=50, blank=True, null=True)  # Field name made lowercase.
    warningandprecautions = models.TextField(db_column='WarningAndPrecautions', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medicationlu'


class Nurse(models.Model):
    medical_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nurse'


class NurseShift(models.Model):
    shift_id = models.IntegerField(primary_key=True)
    medical = models.ForeignKey(Nurse, models.DO_NOTHING, blank=True, null=True)
    shift_type = models.CharField(db_column='Shift_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    start_time = models.TimeField(db_column='Start_Time', blank=True, null=True)  # Field name made lowercase.
    end_time = models.TimeField(db_column='End_Time', blank=True, null=True)  # Field name made lowercase.
    day = models.CharField(db_column='Day', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nurse_shift'


class Patient(models.Model):
    patient_no = models.IntegerField(primary_key=True)  # The composite primary key (patient_no, assessment_id) found, that is not supported. The first column is selected.
    assessment = models.ForeignKey(InitialAssessment, models.DO_NOTHING)
    user = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'
        unique_together = (('patient_no', 'assessment'),)


class Person(models.Model):
    user_id = models.AutoField(primary_key=True)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ssn = models.IntegerField(db_column='SSN', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Prescription(models.Model):
    med_name = models.OneToOneField(Medication, models.DO_NOTHING, db_column='med_name', primary_key=True)  # The composite primary key (med_name, consult_id) found, that is not supported. The first column is selected.
    consult = models.ForeignKey(Encounters, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prescription'
        unique_together = (('med_name', 'consult'),)


class PrevSurgery(models.Model):
    prev_surgery_name = models.CharField(max_length=100)
    history_no = models.OneToOneField(MedicalHis, models.DO_NOTHING, db_column='history_no', primary_key=True)  # The composite primary key (history_no, prev_surgery_name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'prev_surgery'
        unique_together = (('history_no', 'prev_surgery_name'),)


class Receptionist(models.Model):
    receptionist_id = models.IntegerField(primary_key=True)  # The composite primary key (receptionist_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey(Person, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'receptionist'
        unique_together = (('receptionist_id', 'user'),)


class Room(models.Model):
    number = models.IntegerField(primary_key=True)
    d_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='d_name', blank=True, null=True)
    room_type = models.CharField(max_length=20)
    location = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    bit_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room'


class Surgery(models.Model):
    surgery_id = models.IntegerField(primary_key=True)
    s_time = models.TimeField(blank=True, null=True)
    s_date = models.DateField(blank=True, null=True)
    r_number = models.ForeignKey(Room, models.DO_NOTHING, db_column='r_number', blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    anesthesia_type = models.CharField(max_length=30, blank=True, null=True)
    consult = models.ForeignKey(Encounters, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surgery'


class Symptoms(models.Model):
    symptomsid = models.OneToOneField('Symptomslu', models.DO_NOTHING, db_column='SymptomsID', primary_key=True)  # Field name made lowercase. The composite primary key (SymptomsID, consult_id) found, that is not supported. The first column is selected.
    consult = models.ForeignKey(Encounters, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'symptoms'
        unique_together = (('symptomsid', 'consult'),)


class Symptomslu(models.Model):
    symptomsid = models.IntegerField(db_column='SymptomsID', primary_key=True)  # Field name made lowercase.
    symptomsname = models.CharField(db_column='SymptomsName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    symptomscategory = models.CharField(db_column='SymptomsCategory', max_length=100, blank=True, null=True)  # Field name made lowercase.
    onset = models.CharField(db_column='Onset', max_length=100, blank=True, null=True)  # Field name made lowercase.
    associatedfactors = models.TextField(db_column='AssociatedFactors', blank=True, null=True)  # Field name made lowercase.
    associatedconditions = models.TextField(db_column='AssociatedConditions', blank=True, null=True)  # Field name made lowercase.
    aggravatingfactors = models.TextField(db_column='AggravatingFactors', blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50, blank=True, null=True)  # Field name made lowercase.
    severity = models.CharField(db_column='Severity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alleviatingfactors = models.TextField(db_column='AlleviatingFactors', blank=True, null=True)  # Field name made lowercase.
    pattern = models.TextField(db_column='Pattern', blank=True, null=True)  # Field name made lowercase.
    frequency = models.CharField(db_column='Frequency', max_length=50, blank=True, null=True)  # Field name made lowercase.
    additionalnotes = models.TextField(db_column='AdditionalNotes', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'symptomslu'


class Vaccination(models.Model):
    vaccination_name = models.CharField(primary_key=True, max_length=100)  # The composite primary key (vaccination_name, history_no) found, that is not supported. The first column is selected.
    history_no = models.ForeignKey(MedicalHis, models.DO_NOTHING, db_column='history_no')

    class Meta:
        managed = False
        db_table = 'vaccination'
        unique_together = (('vaccination_name', 'history_no'),)


class Visit(models.Model):
    visit_id = models.IntegerField(primary_key=True)
    visit_type = models.CharField(max_length=20, blank=True, null=True)
    discharge_area = models.CharField(max_length=80, blank=True, null=True)
    patient_no = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patient_no', blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visit'
