# grades/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Correctly use the home view
    path('calculate-required-sgpa/', views.calculate_required_sgpa, name='calculate_required_sgpa'),
]
