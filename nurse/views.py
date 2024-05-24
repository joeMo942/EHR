from django.shortcuts import render

def nurse_home(request):
    return render(request, 'nurse/index.html')

def init_assessment(request):
    return render(request, 'nurse/initial-assessment.html')