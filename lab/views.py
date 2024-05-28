from email.message import EmailMessage
from django.shortcuts import redirect, render
from ehr import settings
from patient.models import Test, TestResultField
import io
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
import os
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

@login_required
def lab_home(request):
    user=request.user
    if user.type!='lab':
        raise Http404
    tests=Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, 'lab/index.html', context)

@login_required
def test_result(request , testid):
    user=request.user
    if user.type!='lab':
        raise Http404
    test=Test.objects.get(id=testid)
    if request.method == 'POST':
        print("hello")
        fileds=test.test.testfileds.all()
        for field in fileds:
            result=request.POST.get('result_'+str(field.id))
            result=int(result)
            if result:
                if result>field.refrance_range_up or result<field.refrance_range_down:
                    isupnormal=True
                else:
                    isupnormal=False
            TestResultField.objects.create(
                    testfiled=field,
                    result=int(result),
                    isupnormal=isupnormal,
                    test=test,
                )
        results=TestResultField.objects.filter(test=test)
        contextresult={
            'results':results,
            'test':test
        }
        pdf=get_pdf(contextresult)
        test.result.save(f'test_result_{test.patient.user.first_name}_{test.created_at}.pdf', pdf)
        test.status='Completed'
        
        # current_site = get_current_site(request)
        # mail_subject = 'Activate your account'
        # message = render_to_string('lab/lab_result_email.html')
        # to_email = test.patient.user.email
        # file = test.result  # Assuming test.result is the file you want to attach
        # send_email=EmailMessage(mail_subject, message,settings.EMAIL_HOST_USER , to=[to_email], file=file)
        # send_email.send()

        test.save()
        messages.success(request, 'Test result added successfully')
        return redirect('lab_home')

    context={
        'test':test
    }
    return render(request, 'lab/test-result.html', context)


def get_pdf(context):
    # Render the HTML template with the data
    html = render_to_string('test-result-template.html', context)

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # If there was an error, show it to the user
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')

    # Save PDF to a local file
    buffer.seek(0)
    pdf_file = ContentFile(buffer.read())
    return pdf_file


def send_email(subject, message, recipient_list, file=None):
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list
    )
    if file:
        email.attach(file.name, file.read(), file.content_type)
    email.send()
    return True