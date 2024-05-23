from django.db import models


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    medical_id = models.IntegerField()
    fees = models.IntegerField(blank=True, null=True)


class Doctor(models.Model):
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    user = models.ForeignKey('Person', on_delete=models.CASCADE)
