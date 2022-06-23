from django.db import models


class Faculty(models.Model):
    faculty_id=models.AutoField(primary_key=True)  #Title of thesis
    name=models.CharField(max_length=200)  #name of advisor
    username=models.CharField(max_length=200)  #name of advisor
    password=models.CharField(max_length=120)   #area/domain 
  
class CommitteeMember(models.Model):
    faculty_id=models.ForeignKey(Faculty,on_delete=models.DO_NOTHING)
    thesis_id=models.ForeignKey("Thesis.Thesis",on_delete=models.CASCADE)
  
class Comment(models.Model):
    faculty_id=models.ForeignKey(Faculty,on_delete=models.DO_NOTHING)  ########
    comment=models.TextField()
    thesis_id=models.ForeignKey("Thesis.Thesis",on_delete=models.CASCADE)         ##########
    time=models.TimeField()

class Suggested_topics(models.Model):
    faculty_id=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    topic=models.TextField()
    description=models.TextField(null=True)