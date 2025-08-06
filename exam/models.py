# models.py
from datetime import timezone
from django.db import models
from django.db import models
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    user_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_no = models.CharField(max_length=12)

    def __str__(self):
        return self.user_name

class Photo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.user_name} - {self.id}'
    
    
    

class Question(models.Model):
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return self.text[:50]
    


class UserAnswer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user_name} - Q{self.question.id} - {self.selected_option}"



from django.db import models
from django.contrib.auth.models import User

class ExamWarning(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.reason} - {self.timestamp}"


    
from django.utils import timezone

# models.py
class Snapshot(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='snapshots/', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.employee.user_name} - {self.timestamp}"

