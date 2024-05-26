from . import views
from django.urls import path

urlpatterns = [
    path('', views.lab_home, name='lab_home'),
    path('test-result/', views.test_result, name='test_result'),
]