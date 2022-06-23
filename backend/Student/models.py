from django.db import models
from django.db.models.base import Model

class Student(models.Model):
    student_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    rollno=models.CharField(max_length=15)
    email=models.CharField(max_length=70)
    password=models.CharField(max_length=120)
    status=models.BooleanField()