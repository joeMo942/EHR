from django.db import models
from accounts.models import Account


class Receptionist(models.Model):  

    user = models.models.OneToOneField(Account,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    

