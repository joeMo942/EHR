# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Person(models.Model):
    user_id = models.AutoField(primary_key=True)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ssn = models.IntegerField(db_column='SSN')  # Field name made lowercase.
    password = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=10)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'
