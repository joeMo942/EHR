from django.db import models
from accounts.models import Account


class Receptionist(models.Model):  

    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        
        unique_together = (('receptionist_id', 'user'),)