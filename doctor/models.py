from django.db import models
from accounts.models import Account

class Department(models.Model):
    name = models.CharField(max_length=50,unique=True,blank=False)
    location = models.CharField(max_length=100,blank=True)
    specialization = models.CharField(max_length=50)
    fees = models.IntegerField(default=0,blank=False)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
