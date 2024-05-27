from django.urls import  path
from . import views

urlpatterns = [
    path('', views.nurse_home, name='nurse_home'),
    path('initial-assessment/', views.initial_assessment_view, name='initial_assessment'),
    path('get-full-name/', views.get_full_name, name='get_full_name'),
]
