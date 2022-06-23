from django.db import models
from Student.models import Student
from Faculty.models import Faculty

class Thesis(models.Model):
    thesis_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)  ###############
    advisor_id=models.ForeignKey(Faculty,on_delete=models.DO_NOTHING,to_field="faculty_id")  ##############
    grade=models.CharField(max_length=4,null=True)
    type=models.IntegerField()
    year=models.IntegerField()
    future_work=models.TextField(null=True)
    abstract=models.TextField(null=True)
    thesis_file=models.FileField(null=True,upload_to ='Thesis_Files/')


class Domain(models.Model):
    domain_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=70)


class DomainInfo(models.Model):
    thesis_id=models.ForeignKey(Thesis,on_delete=models.CASCADE)  #######
    domain_id=models.ForeignKey(Domain,on_delete=models.DO_NOTHING)  ###########
  
class DomainFreq(models.Model):
    name=models.CharField(max_length=70, primary_key=True)
    frequency=models.IntegerField()

    class Meta:
        managed = False

class DomainsTrend(models.Model):
    year=models.IntegerField()
    name=models.CharField(max_length=70, primary_key=True)
    frequency=models.IntegerField()

    class Meta:
        managed = False

class Conference(models.Model):
    month=models.CharField(max_length=12)
    name=models.TextField(null=True)
    date=models.CharField(max_length=30)
    link=models.TextField(null=True)
    venue=models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)