from django.db import models

class Admin(models.Model):
    admin_id=models.AutoField(primary_key=True)  #Title of thesis
    name=models.CharField(max_length=200)  #name of student
    username=models.CharField(max_length=200)  #name of advisor
    password=models.CharField(max_length=50)   #area/domain 
  