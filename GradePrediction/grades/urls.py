from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('calculate-required-sgpa/', views.calculate_required_sgpa, name='calculate_required_sgpa'),
]
