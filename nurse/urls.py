from django.urls import  path
from . import views

urlpatterns = [
    path('', views.initial_assessment_view, name='nurse_home'),
    # path('init-assessment/', views.init_assessment, name='init_assessment'),
    path('initial-assessment/', views.initial_assessment_view, name='initial_assessment'),
    path('get-full-name/', views.get_full_name, name='get_full_name'),
]
