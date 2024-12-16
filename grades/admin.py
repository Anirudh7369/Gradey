# grades/admin.py
from django.contrib import admin
from .models import Branch, Subject, Student

admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Student)
