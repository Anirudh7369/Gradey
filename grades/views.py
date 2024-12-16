# grades/views.py
from django.http import JsonResponse
from .models import Subject, Student
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def get_next_sem_credits(branch_id, semester_id):
    if semester_id is None:
        return JsonResponse({"error": "semester_id is missing or invalid."}, status=400)
    
    subjects = Subject.objects.filter(branch_id=branch_id, semester=semester_id + 1)  # Next semester
    total_credits = sum(subject.credit for subject in subjects)
    return total_credits

def calculate_sgpa(current_cgpa, desired_cgpa, completed_credits, next_sem_credits):
    if next_sem_credits == 0:
        raise ValueError("Next semester credits cannot be zero.")
    
    total_credits = completed_credits + next_sem_credits
    required_sgpa = ((desired_cgpa * total_credits) - (current_cgpa * completed_credits)) / next_sem_credits
    return round(required_sgpa, 2)  # Round to 2 decimal places

@csrf_exempt
def calculate_required_sgpa(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            current_cgpa = data.get('current_cgpa')
            desired_cgpa = data.get('desired_cgpa')
            completed_credits = data.get('completed_credits')
            next_sem_credits = data.get('next_sem_credits')
            semester_id = data.get('semester_id')
            branch_id = data.get('branch_id')

            # Check if any required fields are missing
            if not all([current_cgpa, desired_cgpa, completed_credits, next_sem_credits, semester_id, branch_id]):
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            # Check if next_sem_credits is zero
            if next_sem_credits == 0:
                return JsonResponse({"error": "Next semester credits cannot be zero."}, status=400)
            
            # Calculate required SGPA
            required_sgpa = calculate_sgpa(current_cgpa, desired_cgpa, completed_credits, next_sem_credits)
            
            # Return the response with the required SGPA rounded to 2 decimal places as a string
            return JsonResponse({"required_sgpa": f"{required_sgpa:.2f}"})

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Internal server error."}, status=500)

    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


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

# New View for the Root URL
def home(request):
    return render(request, 'index.html')

