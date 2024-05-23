from django.db import models
from accounts.models import Account



class Patient(models.Model):
    patient_no = models.IntegerField(primary_key=True,auto_created=True,blank=False)  # The composite primary key (patient_no, assessment_id) found, that is not supported. The first column is selected.
    # assessment = models.ForeignKey(InitialAssessment, models.DO_NOTHING)
    # nikname=models.CharField(max_length=100)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False,unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"




class MedicalHis(models.Model):
    # history_no = models.AutoField(primary_key=True,auto_created=True)
    patient_no = models.ForeignKey(Patient, on_delete=models.CASCADE,blank=False)
    alcohol = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    high_colest = models.BooleanField(default=False)

    def __str__(self):
       return f"{self.patient_no.user.first_name} {self.patient_no.user.last_name} medical history" 

class Vaccination(models.Model):
    vaccination_name = models.CharField(max_length=100)  # The composite primary key (vaccination_name, history_no) found, that is not supported. The first column is selected.
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