from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,ssn,contact_no,birth_date,gender,type='patient',password=None):
        if not email:
                raise ValueError("User Must Have Email Address")
        
        user =self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                ssn=ssn,
                contact_no=contact_no,
                birth_date=birth_date,
                type=type,
                gender=gender,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            ssn='',
            contact_no='',
            birth_date=None,
            gender=None,
            type='admin',
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True,auto_created=True)
    ssn = models.CharField(max_length=15,unique=True)  # Field name made lowercase.
    password = models.CharField(max_length=128)
    contact_no = models.CharField(max_length=15)
    birth_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=100,unique=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    date_joined =models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)



    USER_TYPES = (
            ('admin', 'Admin'),
            ('receptionist', 'Receptionist'),
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
            ('nurse', 'Nurse'),
            ('lab', 'Lab')
        )
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
    )
    type = models.CharField(max_length=20, blank=True, null=True,choices=USER_TYPES, default='patient')  # Field name made lowercase.
    gender = models.CharField( max_length=10,choices=GENDER_CHOICES, blank=True, null=True)  # Field name made lowercase.

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['first_name','last_name']

    objects =MyAccountManager()


    def __str__(self) :
        return self.email
    
    def has_perm(self,perm ,obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
            return True   