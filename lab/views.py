from django.shortcuts import redirect, render
from ehr import settings
from patient.models import Test, TestResultField
import io
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.files.base import ContentFile


import os
def lab_home(request):
    tests=Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, 'lab/index.html', context)

def test_result(request , testid):

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
        

        test.save()
        messages.success(request, 'Test result added successfully')
        return redirect('lab_home')

    context={
        'test':test
    }
    return render(request, 'lab/test-result.html', context)


def get_pdf(context):
    
    # Render the HTML template with the data
    html = render_to_string('testresulttemplate.html', context)

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
    pdf_name = "test_report.pdf"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), pdf_name), 'wb') as f:
        f.write(buffer.read())

    return HttpResponse(f"PDF saved locally: {pdf_name}")