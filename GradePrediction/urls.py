from django.contrib import admin
from django.urls import path, include
from grades import views  # Import the grades app's views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grades/', include('grades.urls')),  # Delegate grades-related URLs
    path('', views.home, name='home'),  # Root path renders the index.html template
]
