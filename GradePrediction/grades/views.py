# grades/views.py
from django.http import JsonResponse
from .models import Subject, Student
import json

# Calculate Required SGPA
def calculate_required_sgpa(request):
    # Parse JSON data from the request
    data = json.loads(request.body)

    current_cgpa = data.get('current_cgpa')
    desired_cgpa = data.get('desired_cgpa')
    branch_id = data.get('branch_id')
    semester_id = data.get('semester_id')

    # Fetch the student's completed credits and next semester credits
    completed_credits = get_completed_credits(branch_id, semester_id)
    next_sem_credits = get_next_sem_credits(branch_id, semester_id)

    # Calculate the required SGPA
    required_sgpa = calculate_sgpa(current_cgpa, desired_cgpa, completed_credits, next_sem_credits)

    return JsonResponse({'required_sgpa': required_sgpa})

# Helper function to get completed credits for a given semester
def get_completed_credits(branch_id, semester_id):
    subjects = Subject.objects.filter(branch_id=branch_id, semester=semester_id)
    completed_credits = sum(subject.credit_hours for subject in subjects)
    return completed_credits

# Helper function to get the credits for the next semester
def get_next_sem_credits(branch_id, semester_id):
    subjects = Subject.objects.filter(branch_id=branch_id, semester=semester_id + 1)  # Next semester
    next_sem_credits = sum(subject.credit_hours for subject in subjects)
    return next_sem_credits

# Formula to calculate the required SGPA
def calculate_sgpa(current_cgpa, desired_cgpa, completed_credits, next_sem_credits):
    total_credits = completed_credits + next_sem_credits
    required_sgpa = ((desired_cgpa * total_credits) - (current_cgpa * completed_credits)) / next_sem_credits
    return required_sgpa
