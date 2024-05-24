from django.db import models
from accounts.models import Account
from django.core.exceptions import ValidationError



class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    location = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=50)
    fees = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def clean(self):
        if self.user.type != 'doctor':
            raise ValidationError('The associated user must be a doctor.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class AvailabilityTime(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=9, choices=DAYS, blank=True, null=True)

    class Meta:
        unique_together = (('start_time', 'end_time', 'day_of_week'),)

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} - {self.end_time}"

class DoctorAvailability(models.Model):
    availability = models.ForeignKey(AvailabilityTime, on_delete=models.CASCADE)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('doctor', 'availability'),)

    def __str__(self):
        return f"{self.doctor} available at {self.availability}"
