from django.urls import path
from . import views

urlpatterns = [
    path('api/biometric/options/', views.biometric_login_options, name='biometric_options'),
    path('api/biometric/verify/', views.biometric_login_verify, name='biometric_verify'),
]
