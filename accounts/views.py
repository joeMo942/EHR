from django.shortcuts import render

from doctor.models import Doctor
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
            elif user.type == 'receptionist':
                return redirect('receptionist_home')
            elif user.type == 'patient':
                return redirect('patient_home')
            elif user.type == 'nurse':
                return redirect('nurse_home')
            elif user.type == 'admin':
                return redirect('manager_home')
            elif user.type == 'lab':
                return redirect('lab_home')
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

            # if user.type == 'doctor':
            #     Doctor.objects.create(user=user)
            messages.success(request,"The account has been created")
            return redirect('registerstaff')
    else:
        form = RegistrationForm()

    context={
        'form':form
    }
    return render(request, 'accounts/register_staff.html',context)

# Forgot Password
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, EMAIL_HOST_USER ,to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forget-password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/reset-password.html')