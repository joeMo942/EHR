from . import views
from django.urls import path

urlpatterns = [
    path('', views.lab_home, name='lab_home'),
    path('test-result/<int:testid>', views.test_result, name='test_result'),
    path('view-test-result/', views.get_pdf, name='view_test_result'),
]