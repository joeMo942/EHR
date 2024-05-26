from django.shortcuts import render , redirect

def home(request):
    return redirect('login')


# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)