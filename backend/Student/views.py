from django.shortcuts import render
from Student.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import hashlib
from Student.serializers import StudentSerializer
from Admin.serializers import AdminSerializer
from Student.serializers import StudentSerializer
from Thesis.serializers import DomainInfoSerializer, ThesisSerializer
from Faculty.serializers import FacultySerializer,CommitteeMemberSerializer
from Admin.models import Admin
from Thesis.models import Thesis,Domain,DomainInfo
from Student.models import Student
from Faculty.models import Faculty,Comment,CommitteeMember

@api_view(["POST"])
def login_student(request):
        username = request.data.get("username")
        password = request.data.get("password")
        # print(request.data.get("username"))
        # print(request.data.get("password"))
        try:
            Account = Student.objects.get(email=username)
        except Exception:
            return Response({"message":"Incorrect username entered"},status=status.HTTP_400_BAD_REQUEST)
       
        student=User(id=Account.student_id,email=Account.email,password=Account.password)
        student.save()
   
        if student.password!=hashlib.sha256(str.encode(password)).hexdigest():
            return Response({"message":"Incorrect password"},status=status.HTTP_400_BAD_REQUEST)
       
       
        serializer=StudentSerializer(data={"student_id":student.id,"name":Account.name,"email":student.email,"password":student.password},partial=True)
        if serializer.is_valid(raise_exception=True):
            token = Token.objects.get_or_create(user=student)[0].key
            login(request,student,backend='django.contrib.sessions.backends.signed_cookies')
        request.session["username"]=username
        request.session["token"]=token
        request.session["id"]=Account.student_id

        return Response({"message":"User logged in","email":student.username,"token":token},status=status.HTTP_200_OK)


    
@api_view(["GET"])
def student_logout(request):
    try:
        if request.session["token"]:
            request.session.flush()
            return Response({"message":"User logged out"},status=status.HTTP_200_OK)
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def upload_thesis(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except Exception as e:
         return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    
    advisor_name=request.data.get("advisor").title()
    student_name=request.data.get("name").title()
    rollno=request.data.get("rollNo")
    ##Retrieving student id and faculty id 
    student=[{"student_id":student.student_id}
    for student in Student.objects.filter(rollno=rollno)]
    advisor=[{"faculty_id":advisor.faculty_id}
    for advisor in Faculty.objects.filter(name=advisor_name)]
    if not student:
        return Response({"message":"Student not registered"},status=status.HTTP_400_BAD_REQUEST)
    
    type=request.data.get("type")
    title=request.data.get("title").title()
    year=request.data.get("year")
    futureWork=request.data.get("futureWork")
    grade=request.data.get("grade").title()
    flag1=False
    flag2=False
    
    if request.data.get("fileDoc"):
          flag1=True
          
    if request.data.get("abstract"):
        flag2=True
        abstract=request.data.get("abstract")
    
    if flag1==True and flag2==True: #when abstract and file both have been entered
        _, file = request.FILES.popitem()
        file = file[0]
        serializer=ThesisSerializer(data={"title":title,"student_id":student[0].get("student_id"),"advisor_id":advisor[0].get("faculty_id"),"type":type,"year":year,
        "abstract":abstract,"grade":grade,"thesis_file":file,"future_work":futureWork},partial=True)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            
        
    if flag1==False and flag2==True: #when only abstract has been entered by user
        serializer=ThesisSerializer(data={"title":title,"student_id":student[0].get("student_id"),"advisor_id":advisor[0].get("faculty_id"),"type":type,"year":year,
        "abstract":abstract,"future_work":futureWork,"grade":grade},partial=True)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()

    thesis=Thesis.objects.last()
    thesis_id=thesis.thesis_id

    cm1=request.data.get("cm1")
    cm2=request.data.get("cm2")
    cm3=request.data.get("cm3")

    if cm1!="Choose one":
        fac1=[{"faculty_id":fac1.faculty_id}
        for fac1 in Faculty.objects.filter(name=cm1.title())]
        comm_serializer1=CommitteeMemberSerializer(data={"thesis_id":thesis_id,"faculty_id":fac1[0].get("faculty_id")})
        if comm_serializer1.is_valid():
            comm_serializer1.save()
    
    if cm2!="Choose one":
        fac2=[{"faculty_id":fac2.faculty_id}
        for fac2 in Faculty.objects.filter(name=cm2.title())]
        comm_serializer2=CommitteeMemberSerializer(data={"thesis_id":thesis_id,"faculty_id":fac2[0].get("faculty_id")})
        if comm_serializer2.is_valid():
            comm_serializer2.save()
    
    if cm3!="Choose one":
        fac3=[{"faculty_id":fac3.faculty_id}
        for fac3 in Faculty.objects.filter(name=cm3.title())]
        comm_serializer3=CommitteeMemberSerializer(data={"thesis_id":thesis_id,"faculty_id":fac3[0].get("faculty_id")})
        if comm_serializer3.is_valid():
            comm_serializer3.save()
    
    dom=request.data.get("domain")

    for j in range(len(dom)):
        domain=[{"domain_id":domain.domain_id}
        for domain in Domain.objects.filter(name=dom[j].get("domain").title())]
        dom_serializer=DomainInfoSerializer(data={"thesis_id":thesis_id,"domain_id":domain[0].get("domain_id")})
        if dom_serializer.is_valid():
            dom_serializer.save()
    return Response({"message":"Thesis added successfuly"},status=status.HTTP_200_OK)


@api_view(["PATCH"])
def edit_thesis(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except Exception as e:
         return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    print(request.data.get("fileDoc"))
    advisor_name=request.data.get("advisor").title()
    student_name=request.data.get("name").title()
    rollno=request.data.get("rollNo")
    ##Retrieving student id and faculty id 
    student=[{"student_id":student.student_id}
    for student in Student.objects.filter(rollno=rollno)]
    advisor=[{"faculty_id":advisor.faculty_id}
    for advisor in Faculty.objects.filter(name=advisor_name)]
    if not student:
        return Response({"message":"Student not registered"},status=status.HTTP_400_BAD_REQUEST)
    
    type=request.data.get("type")
    title=request.data.get("title").title()
    year=request.data.get("year")
    futureWork=request.data.get("futureWork")
    grade=request.data.get("grade").title()
    thesis_id=request.data.get("thesis_id")
    flag1=False
    flag2=False
    
    if request.data.get("fileDoc"):
          flag1=True
          
    if request.data.get("abstract"):
        flag2=True
        abstract=request.data.get("abstract")
    
    if flag1==True and flag2==True: #when abstract and file both have been entered
        _, file = request.FILES.popitem()
        file = file[0]
        thesis=Thesis.objects.get(thesis_id=thesis_id)
        serializer=ThesisSerializer(thesis,data={"title":title,"student_id":student[0].get("student_id"),"advisor_id":advisor[0].get("faculty_id"),"type":type,"year":year,
        "abstract":abstract,"grade":grade,"thesis_file":file,"future_work":futureWork},partial=True)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            
        
    if flag1==False and flag2==True: #when only abstract has been entered by user
        thesis=Thesis.objects.get(thesis_id=thesis_id)
        serializer=ThesisSerializer(thesis,data={"title":title,"student_id":student[0].get("student_id"),"advisor_id":advisor[0].get("faculty_id"),"type":type,"year":year,
        "abstract":abstract,"future_work":futureWork,"grade":grade},partial=True)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()

    thesis=Thesis.objects.last()
    thesis_id=thesis.thesis_id

    cm1=request.data.get("cm1")
    cm2=request.data.get("cm2")
    cm3=request.data.get("cm3")

    if cm1!="Choose one":
        fac1=[{"faculty_id":fac1.faculty_id}
        for fac1 in Faculty.objects.filter(name=cm1.title())]
        comm_member=CommitteeMember.objects.get(faculty_id=fac1[0].get("faculty_id"))
        comm_serializer1=CommitteeMemberSerializer(comm_member,data={"thesis_id":thesis_id,"faculty_id":fac1[0].get("faculty_id")})
        if comm_serializer1.is_valid():
            comm_serializer1.save()
    
    if cm2!="Choose one":
        fac2=[{"faculty_id":fac2.faculty_id}
        for fac2 in Faculty.objects.filter(name=cm2.title())]
        comm_member=CommitteeMember.objects.get(faculty_id=fac2[0].get("faculty_id"))
        comm_serializer2=CommitteeMemberSerializer(comm_member,data={"thesis_id":thesis_id,"faculty_id":fac2[0].get("faculty_id")})
        if comm_serializer2.is_valid():
            comm_serializer2.save()
    
    if cm3!="Choose one":
        fac3=[{"faculty_id":fac3.faculty_id}
        for fac3 in Faculty.objects.filter(name=cm3.title())]
        comm_member=CommitteeMember.objects.get(faculty_id=fac3[0].get("faculty_id"))
        comm_serializer3=CommitteeMemberSerializer(comm_member,data={"thesis_id":thesis_id,"faculty_id":fac3[0].get("faculty_id")})
        if comm_serializer3.is_valid():
            comm_serializer3.save()
    
    dom=request.data.get("domain")

    for j in range(len(dom)):
        domain=[{"domain_id":domain.domain_id}
        for domain in Domain.objects.filter(name=dom[j].get("domain").title())]
        dom=Domain.objects.get(domain_id=domain[0].get("domain_id"))
        dom_serializer=DomainInfoSerializer(dom,data={"thesis_id":thesis_id,"domain_id":domain[0].get("domain_id")})
        if dom_serializer.is_valid():
            dom_serializer.save()
    return Response({"message":"Thesis added successfuly"},status=status.HTTP_200_OK)

