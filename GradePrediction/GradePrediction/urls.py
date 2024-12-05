from django.contrib import admin
from django.urls import path, include  # Import include to reference app URLs

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin interface
    path('grades/', include('grades.urls')),  # Include URLs from the grades app
]
