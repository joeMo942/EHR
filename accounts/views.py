from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from patient.models import Patient  

# Activation Email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from ehr.settings import EMAIL_HOST_USER


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            contact_no=form.cleaned_data['contact_no']
            password=form.cleaned_data['password']
            ssn=form.cleaned_data['ssn']
            birth_date=form.cleaned_data['birth_date']
            gender=form.cleaned_data['gender']

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,ssn=ssn,birth_date=birth_date,contact_no=contact_no,
                                            gender=gender,password=password)
            user.save()
            messages.success(request,"yesssss")
            # return redirect('register')


            # Activation Email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message ,EMAIL_HOST_USER,to=[to_email])
            
            try:
                send_mail.send()
                messages.success(request, "Activation link has been sent to your email.")
            except Exception as e:
                messages.error(request, "There was an error sending the activation email. Please try again later.")

            # return redirect('accounts/login/?command=verfication&email='+ email)
            return redirect('login')
    else:
        form = RegistrationForm()

    context={
        'form':form
    }
    return render(request, 'accounts/register.html',context)


def avtivation(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(ValueError,OverflowError,TypeError,Account.DoesNotExist):
        user=None
    
    if user is not None:
        if default_token_generator.check_token(user,token):
            user.is_active=True
            Patient.objects.create(user=user)
            user.save()
            messages.success(request,"Account has been activated")
            return redirect('login')
        else:
            messages.error(request,"Activation link is invalid")
            return redirect('register')
    else:
        messages.error(request,"User not found")
        return redirect('register')

def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            print(user.type)
            if user.type == 'doctor':
                return redirect('doctor_home')
            else:
                return redirect('patient_home')
        else:
            messages.error(request,"Invalid login Email or Password")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')


def registerstaff(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            contact_no=form.cleaned_data['contact_no']
            password=form.cleaned_data['password']
            ssn=form.cleaned_data['ssn']
            birth_date=form.cleaned_data['birth_date']
            gender=form.cleaned_data['gender']
            type=form.cleaned_data['type']


            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,ssn=ssn,birth_date=birth_date,contact_no=contact_no,
                                            gender=gender,type=type,password=password)
            user.is_staff=True
            user.is_active=True

            user.save()
            messages.success(request,"The account has been created")
            return redirect('registerstaff')
    else:
        form = RegistrationForm()

    context={
        'form':form
    }
    return render(request, 'accounts/register_staff.html',context)
