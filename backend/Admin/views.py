
from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from Admin.serializers import AdminSerializer
from Student.serializers import StudentSerializer
from Thesis.serializers import ThesisSerializer, DomainSerializer
from Faculty.serializers import FacultySerializer,CommitteeMemberSerializer
from Admin.models import Admin
from Thesis.models import Thesis,Domain,DomainInfo
from Student.models import Student
from Faculty.models import Faculty,Comment,CommitteeMember
from django.db.models import Q
import hashlib
from Thesis.serializers import DomainInfoSerializer
from django.core.files.storage import FileSystemStorage


@api_view(["POST"])
def login_admin(request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            Account = Admin.objects.get(username=username)
        except Exception:
            return Response({"message":"Incorrect username entered"},status=status.HTTP_400_BAD_REQUEST)
        
        
        admin=User(id=Account.admin_id,username=Account.username,password=Account.password)
        admin.save()
        if admin.password==password or admin.password==hashlib.sha256(str.encode(password)).hexdigest():
            serializer=AdminSerializer(data={"admin_id":admin.id,"name":Account.name,"username":admin.username,"password":admin.password})
            if serializer.is_valid(raise_exception=True):
                token = Token.objects.get_or_create(user=admin)[0].key
                print(token)
                login(request, admin,backend='django.contrib.auth.backends.ModelBackend')
            
            request.session["username"]=username
            request.session["token"]=token
            request.session["id"]=Account.admin_id

            return Response({"message":"User logged in","email":admin.username,"token":token,"user":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Incorrect password"},status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(["GET"])
def logout_admin(request):
    try:
        if request.session["token"]:
            request.session.flush()
            return Response({"message":"User logged out"},status=status.HTTP_200_OK)
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

##Edit Thesis
@api_view(['PATCH'])
def thesis_edit(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    thesis_id=request.data.get("thesis_id")

    if request.data.get("type"):
        type=request.data.get("type")
    if request.data.get("year"):
        year=request.data.get("year")
        try:
            val = int(year)
        except ValueError:
            return Response({"message":"Incorrect format of data field 'Year'"},status=status.HTTP_400_BAD_REQUEST)
    if request.data.get("grade"):
        grade=request.data.get("grade")
    if request.data.get("title"):
        title=request.data.get("title")
        title=title.title()
    if request.data.get("abstract"):
        abstract=request.data.get("abstract")
   
    thesis=Thesis.objects.get(thesis_id=thesis_id)
    serializer=ThesisSerializer(thesis,data={"year":year, "grade":grade,"abstract":abstract, "type":type, "title": title},partial=True)
   
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Thesis edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Thesis not edited"},status=status.HTTP_400_BAD_REQUEST)



##View complete details of a thesis
@api_view(['POST'])
def thesis_view(request):   
    try:
        if request.session["token"]:
            admin_id=request.session["id"]

    except Exception as e:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    thesis_id=request.data.get("thesis_id")        
    student_info=[]
    advisor_info=[]
    committee_mems=[]
    domains=[]
    thesis=[{"thesis_id":thesis.thesis_id,"title":thesis.title,"student_id":thesis.student_id,"advisor_id":thesis.advisor_id,"grade":thesis.grade,"type":thesis.type,"year":thesis.year,"abstract":thesis.abstract,"future_work":thesis.future_work}
            for thesis in Thesis.objects.filter(thesis_id=thesis_id)]
    for object in thesis:
        std=object.get("student_id")
        student=[{"name":student.name,"rollno":student.rollno}
        for student in Student.objects.filter(student_id=std.student_id)]
        student_info.extend(student)
        object.pop("student_id")
          
    for object2 in thesis:
        ad=object2.get("advisor_id")
        advisor=[{"name":advisor.name}
        for advisor in Faculty.objects.filter(faculty_id=ad.faculty_id)]
        advisor_info.extend(advisor)
        object2.pop("advisor_id")

    for object3 in thesis:
        id=object3.get("thesis_id")
        domain_info=[{"thesis_id":domain_info.thesis_id,"domain_id":domain_info.domain_id}
                    for domain_info in DomainInfo.objects.filter(thesis_id=id)]
        for i in range (len(domain_info)):
            domain=domain_info[i].get("domain_id")
            dom_id=domain.domain_id
            dom_names=[{"name":dom_names.name}
            for dom_names in Domain.objects.filter(domain_id=dom_id)]
            domains.extend(dom_names)

    for object4 in thesis:
        id=object4.get("thesis_id")
        
        committee_mem=[{"thesis_id":committee_mem.thesis_id,"faculty_id":committee_mem.faculty_id}
                    for committee_mem in CommitteeMember.objects.filter(thesis_id=id)]
        for i in range(len(committee_mem)):
            committee=committee_mem[i].get("faculty_id")
            fac_id=committee.faculty_id
            com_names=[{"name":com_names.name}
            for com_names in Faculty.objects.filter(faculty_id=fac_id)]
            committee_mems.extend(com_names)
    return Response({"student":student_info,"advisor":advisor_info,"domain":domains,"thesis":thesis, "committeeMembers": committee_mems},status=status.HTTP_200_OK)
            
@api_view(["POST"])
def register_student(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    
    name=request.data.get("name")
    name=name.title()
    rollno=request.data.get("rollno")
    rollno=rollno.upper()
    email=request.data.get("email")
    email=email.lower()
    std_status=request.data.get("std_status")
    password=request.data.get("password")
    status2=1
    if std_status=="current":
        status2=1
    else:
        status2=0
    
    if (name=="" or rollno=="" or email=="" or std_status==""):
        return Response({"message":"Enter all fields!"},status=status.HTTP_400_BAD_REQUEST)

    else:
        flag1=False
        flag2=False

        student1=[{"name":student1.name,"rollno":student1.rollno,"email":student1.email, "status": student1.status}
            for student1 in Student.objects.filter(rollno=rollno)]
        if student1:
            std=student1[0].get("rollno") 
            if std==rollno:
                flag1=True

        student2=[{"name":student2.name,"rollno":student2.rollno,"email":student2.email, "status": student2.status}
            for student2 in Student.objects.filter(email=email)]

        if student2:
            std2=student2[0].get("email") 
            if std2==email:
                flag2=True

        if flag1==True or flag2==True:
            return Response({"message":"Student already registered!"},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            enc_string=hashlib.sha256(str.encode(password)).hexdigest()
            serializer=StudentSerializer(data={"name":name,"rollno": rollno,"email":email,"username":name, "password": enc_string, "status":status2})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Student registered successfully!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Student not registered!"},status=status.HTTP_400_BAD_REQUEST)
                
@api_view(["POST"])
def register_faculty(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    name=request.data.get("name")
    name=name.title()
    username=request.data.get("username")
    username=username.lower()
    password=request.data.get("password")
    
    if (name=="" or username==""):
        return Response({"message":"Enter all fields!"},status=status.HTTP_400_BAD_REQUEST)
    
    else:
        flag1=False

        faculty=[{"name":faculty.name,"username":faculty.username}
            for faculty in Faculty.objects.filter(username=username)]
        if faculty:
            fac=faculty[0].get("username") 
            if fac==username:
                flag1=True

        if flag1==True:
            return Response({"message":"Faculty member already registered!"},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            enc_string=hashlib.sha256(str.encode(password)).hexdigest()
            serializer=FacultySerializer(data={"name":name,"username": username,"password": enc_string})
            if serializer.is_valid(raise_exception=True):
                serializer.save() 
                return Response({"message":"Faculty member registered successfully!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Faculty member not registered!"},status=status.HTTP_400_BAD_REQUEST)

#View a list of all students
@api_view(['GET'])
def view_students(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    student_info=[]
    student=[{"student_id":student.student_id,"name":student.name,"rollno":student.rollno,"email":student.email,"status":student.status}
                        for student in Student.objects.filter()]
    if student:
        student_info.extend(student)
    
        return Response({"students":student_info},status=status.HTTP_200_OK)
    else:
        return Response({"message":"No results found!"},status=status.HTTP_204_NO_CONTENT)

#View a list of all faculty members
@api_view(['GET'])
def view_faculty(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    faculty_info=[]
    faculty=[{"faculty_id":faculty.faculty_id,"name":faculty.name, "username":faculty.username}
                        for faculty in Faculty.objects.filter()]
    if faculty:
        faculty_info.extend(faculty)
    
        return Response({"faculty":faculty_info},status=status.HTTP_200_OK)
    else:
        return Response({"message":"No results found!"},status=status.HTTP_204_NO_CONTENT)
     
@api_view(['PATCH'])
def edit_faculty(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    id=request.data.get("faculty_id")
    faculty=Faculty.objects.get(faculty_id=id)

    if request.data.get("name"):
        name=request.data.get("name")
        name=name.title()
    if request.data.get("username"):
        username=request.data.get("username")
        username=username.lower()
    enc_string="-1"
    if request.data.get("password"):
        password=request.data.get("password")
        enc_string=hashlib.sha256(str.encode(password)).hexdigest()

    flag=False
    check_fac=[{"username":check_fac.username}
    for check_fac in Faculty.objects.filter(faculty_id=id)]
    if(username!=check_fac[0].get("username")):
         FacCheck=[{"username":FacCheck.username}
            for FacCheck in Faculty.objects.filter(username=username)]
         if FacCheck:
             fac=FacCheck[0].get("username") 
             if fac==username:
                 flag=True
    
    if flag==True:
             return Response({"message":"Existing email can't be used!"},status=status.HTTP_400_BAD_REQUEST)
    
    if enc_string!="-1":
        serializer=FacultySerializer(faculty,data={"name":name,"username":username, "password":enc_string},partial=True) 
    else:
        serializer=FacultySerializer(faculty,data={"name":name,"username":username},partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Faculty member edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Faculty member not edited"},status=status.HTTP_400_BAD_REQUEST)

##edit details of a student
@api_view(['PATCH'])
def edit_student(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    id=request.data.get("student_id")
    student=Student.objects.get(student_id=id)
    flag1=False
    flag2=False

    if request.data.get("name"):
        n=request.data.get("name")
        name=n.title()
    if request.data.get("rollno"):
        rollno=request.data.get("rollno")
        rollno=rollno.upper()
    if request.data.get("email"):
        email=request.data.get("email")
        email=email.lower()

    enc_string="-1"
    if request.data.get("password"):
        password=request.data.get("password")
        enc_string=hashlib.sha256(str.encode(password)).hexdigest()

    check_std=[{"name":check_std.name,"rollno":check_std.rollno,"email":check_std.email}
    for check_std in Student.objects.filter(student_id=id)]
    if(rollno!=check_std[0].get("rollno")):
         StdCheck=[{"rollno":StdCheck.rollno}
            for StdCheck in Student.objects.filter(rollno=rollno)]
         if StdCheck:
             std=StdCheck[0].get("rollno") 
             if std==rollno:
                 flag1=True
                 
    if(email!=check_std[0].get("email")):
        ##checks if the new email already exists
        StdCheck2=[{"email":StdCheck2.email}
            for StdCheck2 in Student.objects.filter(email=email)]
        if StdCheck2:
            std2=StdCheck2[0].get("email") 
            if std2==email:
                flag2=True

    std_status="-1"
    if request.data.get("status"):
        stat=request.data.get("status")
        if stat=="current":
            std_status=1
        else:
            std_status=0

    if flag1==True or flag2==True:
             return Response({"message":"Existing email or roll number can't be used!"},status=status.HTTP_400_BAD_REQUEST)
    if std_status!="-1" and enc_string!="-1":
        serializer=StudentSerializer(student,data={"name":name,"email":email, "rollno":rollno, "status":std_status, "password": enc_string},partial=True)
    elif enc_string!="-1":
        serializer=StudentSerializer(student,data={"name":name,"email":email, "rollno":rollno, "password": enc_string},partial=True)
    elif std_status!="-1":
        serializer=StudentSerializer(student,data={"name":name,"email":email, "rollno":rollno, "status":std_status},partial=True)
    else:
        serializer=StudentSerializer(student,data={"name":name,"email":email, "rollno":rollno},partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Student edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Student not edited"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_faculty(request,id):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    faculty=Faculty.objects.get(faculty_id=id)
    faculty.delete()
    return Response({"message":"Faculty memeber deleted successfully"},status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_student(request,id):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    student=Student.objects.get(student=id)
    student.delete()
    return Response({"message":"Student deleted successfully"},status=status.HTTP_200_OK)

##to view comments
@api_view(['POST'])
def view_comments(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    thesis_id=request.data.get("thesis_id")   
    comments=[{"thesis_id":comments.thesis_id,"faculty_id":comments.faculty_id,"comment":comments.comment,"time":comments.time}
                for comments in Comment.objects.filter(thesis_id=thesis_id)]
    if comments:
        faculty_names=[]
        for obj in comments:
            fac=obj.get("faculty_id")
            fac_info=[{"name":fac_info.name}
            for fac_info in Faculty.objects.filter(faculty_id=fac.faculty_id)]
            faculty_names.extend(fac_info)
            obj.pop("faculty_id")
            obj.pop("thesis_id")
        
        return Response({"comments":comments,"faculty":faculty_names},status=status.HTTP_200_OK)
    else:
        return Response({"message":"No comments for this thesis"},status=status.HTTP_200_OK)

##Edit Thesis
@api_view(['POST'])
def change_password(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    username=request.data.get("username")
    username=username.lower()

    old_password=request.data.get("old_password")
    new_password=request.data.get("new_password")
    confirm_password=request.data.get("confirm_password")

    if old_password=="" or new_password=="" or confirm_password=="":
        return Response({"message":"Enter all fields!"},status=status.HTTP_400_BAD_REQUEST)
    
    else:
        flag1=False
        admin1=[{"password":admin1.password}
                for admin1 in Admin.objects.filter(username=username)]
        if admin1:
            adm_pass=admin1[0].get("password") 
            if adm_pass!=old_password:
                return Response({"message":"Incorrect old password!"},status=status.HTTP_400_BAD_REQUEST)
            else:
                min_length=6
                first_isalpha = new_password[0].isalpha()
                if len(new_password)<min_length:
                    return Response({"message":"The new password must be at least %d characters long" %min_length},status=status.HTTP_400_BAD_REQUEST)
                if all(c.isalpha() == first_isalpha for c in new_password):
                    return Response({"message":"The new password must contain at least one character and at least one digit." },status=status.HTTP_400_BAD_REQUEST)
                if new_password!=confirm_password:
                    return Response({"message":"New and confirm password must be same."},status=status.HTTP_400_BAD_REQUEST)
                else:
                    admin= Admin.objects.get(username=username)
                    serializer=AdminSerializer(admin,data={"password":new_password, "name":admin.name, "username":admin.username})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"message":"Password changed succesfully!"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Password not changed!"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def view_faculty_detail(request):   
    try:
        if request.session["token"]:
            admin_id=request.session["id"]

    except Exception as e:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
   
    id=request.data.get("faculty_id")
    faculty=[{"faculty_id":faculty.faculty_id,"name":faculty.name,"username":faculty.username}
            for faculty in Faculty.objects.filter(faculty_id=id)]
   
    
    return Response({"faculty":faculty},status=status.HTTP_200_OK)

@api_view(["POST"])
def view_student_detail(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]

    except Exception as e:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    student_id=request.data.get("student_id")
    student=[{"student_id":student.student_id,"name":student.name,"rollno":student.rollno,"email":student.email,"status":student.status}
                        for student in Student.objects.filter(student_id=student_id)]
    return Response({"student":student},status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_thesis(request):
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

@api_view(["POST"])
def search_faculty_list(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except Exception as e:
         return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    name=request.data.get("name")
    words=name.split(" ")
    result=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Faculty.objects.filter(Q(name__icontains=words[i].title()))
            if query:
                result.extend(query)
    
    output=[]
    faculty=[]

    for i in range(len(result)):
        output=[{"faculty_id":output.faculty_id,"name":output.name,"username":output.username}
        for output in Faculty.objects.filter(faculty_id=result[i].faculty_id)]
        if output[0] not in faculty:
            faculty.extend(output)
            output.clear()
        else:
            output.clear()

    if len(faculty)==0:
        return Response({"message":"No faculty member found"},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"faculty":faculty},status=status.HTTP_200_OK)

@api_view(["POST"])
def search_student_list(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except Exception as e:
         return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    name=request.data.get("name")
    words=name.split(" ")
    result=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Student.objects.filter(Q(name__icontains=words[i].title()))
            if query:
                result.extend(query)
    
    output=[]
    students=[]

    for i in range(len(result)):
        output=[{"student_id":output.student_id,"name":output.name,"email":output.email,"rollno":output.rollno}
        for output in Student.objects.filter(student_id=result[i].student_id)]
        if output[0] not in students:
            students.extend(output)
            output.clear()
        else:
            output.clear()
            
    if len(students)==0:
        return Response({"message":"No student found"},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"students":students},status=status.HTTP_200_OK)

@api_view(["POST"])
def add_domain(request):
    try:
        if request.session["token"]:
            admin_id=request.session["id"]
    except Exception as e:
         return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    name=request.data.get("domain").lower().title()
    domain=[{"domain_id":domain.domain_id,"name":domain.name}
    for domain in Domain.objects.filter(name=name)]
    if not domain:
        max_id = Domain.objects.filter().order_by('domain_id').last().domain_id
        domain_id=max_id+1
        serializer=DomainSerializer(data={"domain_id":domain_id,"name":name},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Domain name saved"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Domain name not saved"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Domain name already present"},status=status.HTTP_400_BAD_REQUEST)