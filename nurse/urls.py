from django.urls import  path
from . import views

urlpatterns = [
    path('', views.nurse_home, name='nurse_home'),
    path('initial-assessment/', views.init_assessment, name='init_assessment'),
]
