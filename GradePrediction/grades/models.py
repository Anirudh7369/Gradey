from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    credit_hours = models.FloatField()
    semester = models.IntegerField()

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    current_cgpa = models.FloatField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.IntegerField()

    def __str__(self):
        return self.name
