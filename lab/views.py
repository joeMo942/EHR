from django.shortcuts import render

def lab_home(request):
    return render(request, 'lab/index.html')

def test_result(request):
    return render(request, 'lab/test-result.html')