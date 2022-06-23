
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import set_rollback
from Thesis.serializers import ThesisSerializer
from Faculty.serializers import CommitteeMemberSerializer,FacultySerializer,CommentSerializer,SugestedTopicsSerializer
from Faculty.models import Faculty,CommitteeMember,Comment,Suggested_topics
from Thesis.models import Thesis,DomainInfo,Domain
from Student.models import Student
from datetime import datetime
import hashlib
from django.db.models import Q


@api_view(["POST"])
def login_faculty(request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            Account = Faculty.objects.get(username=username)
        except Exception:
            return Response({"message":"Incorrect username entered"},status=status.HTTP_400_BAD_REQUEST)
        
        faculty=User(id=Account.faculty_id,username=Account.username,password=Account.password)
        faculty.save()
    
        if faculty.password!=hashlib.sha256(str.encode(password)).hexdigest():
            return Response({"message":"Incorrect password"},status=status.HTTP_400_BAD_REQUEST)
        
       
        serializer=FacultySerializer(data={"faculty_id":faculty.id,"name":Account.name,"username":faculty.username,"password":faculty.password})
        if serializer.is_valid(raise_exception=True):
            token = Token.objects.get_or_create(user=faculty)[0].key
            login(request, faculty,backend='django.contrib.sessions.backends.signed_cookies')
        request.session["username"]=username
        request.session["token"]=token
        request.session["id"]=Account.faculty_id

        return Response({"message":"User logged in","email":faculty.username,"token":token},status=status.HTTP_200_OK)
        
        
    
@api_view(["GET"])
def faculty_logout(request):
    try:
        if request.session["token"]:
            request.session.flush()
            return Response({"message":"User logged out"},status=status.HTTP_200_OK)
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)


########API to get the list of theses where the logged in faculity member is a committee member
@api_view(["GET"])
def show_evaluated_thesis(request):
    try:
        if request.session["token"]:           ##Checks if the user is logged in 
            id=request.session.get("id")         #Gets id of the logged in faculty member
    except Exception as e:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    output=[]
    info=[{"thesis_id":info.thesis_id,"faculty_id":info.faculty_id}   #Gets the info of thesis that the faculty member has evaluated
    for info in CommitteeMember.objects.filter(faculty_id=id)]
    if info:
        length=len(info)
        for i in range(length):
            thesis_id=info[i].get("thesis_id")         #Retrieve those theses from the thesis table
            thesis=[{"thesis_id":thesis.thesis_id,"title":thesis.title,"student_id":thesis.student_id,"advisor_id":thesis.advisor_id,"grade":thesis.grade,"type":thesis.type,"year":thesis.year,"abstract":thesis.abstract}
                   for thesis in Thesis.objects.filter(thesis_id=thesis_id.thesis_id)]
            if thesis:
                    output.extend(thesis)

        student_info=[]
        advisor_info=[]
        domains=[]
                ####The data retrieved from Thesis table has foreign key values.
                ###Following code retrieves values of those foreign keys and places the data into seperate arrays
        for object in output:
            std=object.get("student_id")
            student=[{"name":student.name,"rollno":student.rollno}
            for student in Student.objects.filter(student_id=std.student_id)]
            student_info.extend(student)
            object.pop("student_id")
     
        for object2 in output:
            ad=object2.get("advisor_id")
            advisor=[{"name":advisor.name}
            for advisor in Faculty.objects.filter(faculty_id=ad.faculty_id)]
            advisor_info.extend(advisor)
            object2.pop("advisor_id")

        for object3 in output:
            id=object3.get("thesis_id")
            domain_info=[{"thesis_id":domain_info.thesis_id,"domain_id":domain_info.domain_id}
            for domain_info in DomainInfo.objects.filter(thesis_id=id)]
            domain=domain_info[0].get("domain_id")
            dom_id=domain.domain_id
            dom_names=[{"name":dom_names.name}
            for dom_names in Domain.objects.filter(domain_id=dom_id)]
            domains.extend(dom_names)

        return Response({"students":student_info,"advisors":advisor_info,"domains":domains,"thesis":output},status=status.HTTP_200_OK)
    else:
         return Response({"message":"No evaluated thesis"},status=status.HTTP_204_NO_CONTENT)
    

###API to get list of theses the logged in faculty member has supervised
@api_view(['GET'])
def show_supervided_thesis(request):
    try:
        if request.session["token"]:
            id=request.session["id"]
    except Exception as e:
        print(e)
        return Response({"message":"User is not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    student_info=[]
    advisor_info=[]
    domains=[]
    thesis=[{"thesis_id":thesis.thesis_id,"title":thesis.title,"student_id":thesis.student_id,"advisor_id":thesis.advisor_id,"grade":thesis.grade,"type":thesis.type,"year":thesis.year,"abstract":thesis.abstract}
               for thesis in Thesis.objects.filter(advisor_id=id)]
    if thesis:
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
            domain=domain_info[0].get("domain_id")
            dom_id=domain.domain_id
            dom_names=[{"name":dom_names.name}
            for dom_names in Domain.objects.filter(domain_id=dom_id)]
            domains.extend(dom_names)

        print(student_info)
        print(advisor_info)
        print(domains)
        return Response({"students":student_info,"advisors":advisor_info,"domains":domains,"thesis":thesis},status=status.HTTP_200_OK)
    else:
        return Response({"message":"No supervised theses"},status=status.HTTP_204_NO_CONTENT)
    

##API to view Thesis for logged in faculty (when the thesis is clicked on to view details)
@api_view(['POST'])
def view_thesis(request):   
    try:
        if request.session["token"]:
            fac_id=request.session["id"]

    except Exception as e:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
            
    student_info=[]
    advisor_info=[]
    domains=[]
    members=[]
    id=request.data.get("thesis_id")
    thesis=[{"thesis_id":thesis.thesis_id,"title":thesis.title,"student_id":thesis.student_id,"advisor_id":thesis.advisor_id,"grade":thesis.grade,"type":thesis.type,"year":thesis.year,"abstract":thesis.abstract,"future_work":thesis.future_work}
            for thesis in Thesis.objects.filter(thesis_id=id)]
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
        for i in range(0,len(domain_info)):
            domain=domain_info[i].get("domain_id")
            dom_id=domain.domain_id
            dom_names=[{"name":dom_names.name}
            for dom_names in Domain.objects.filter(domain_id=dom_id)]
            domains.extend(dom_names)

    com_members=[{"faculty_id":com_members.faculty_id,"thesis_id":com_members.thesis_id}
    for com_members in CommitteeMember.objects.filter(thesis_id=id)]

    for obj4 in com_members:
        faculty_id=obj4.get("faculty_id").faculty_id
        info=[{"name":info.name}
        for info in Faculty.objects.filter(faculty_id=faculty_id)]
        members.extend(info)
    return Response({"student":student_info,"advisor":advisor_info,"domain":domains,"thesis":thesis,"members":members},status=status.HTTP_200_OK)

@api_view(["POST"])
def search_by_topic_supervised_thesis(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topics=request.data.get("topic")

    words=topics.split(" ")
    result=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Thesis.objects.filter(Q(title__icontains=words[i].title()))
            if query:
                result.extend(query)
                
    thesis=[]
    output=[]
    for j in range(len(result)):
        output=[{"thesis_id":output.thesis_id,"title":output.title,"student_id":output.student_id,"advisor_id":output.advisor_id,"grade":output.grade,"type":output.type,"year":output.year,"abstract":output.abstract}
        for output in Thesis.objects.filter(thesis_id=result[j].thesis_id)]
        if output[0].get("advisor_id").faculty_id==fac_id and output[0] not in thesis:
            thesis.extend(output)
            output.clear()
        else:
            output.clear()
    
    if len(thesis)!=0:
        student_info=[]
        advisor_info=[]
    
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
        
        return Response({"student":student_info,"advisor":advisor_info,"thesis":thesis},status=status.HTTP_200_OK)
    else:
        return Response({"message":"No thesis found"},status=status.HTTP_404_NOT_FOUND)
  
@api_view(["POST"])
def search_by_topic_evaluated_thesis(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topics=request.data.get("topic")

    words=topics.split(" ")
    result=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Thesis.objects.filter(Q(title__icontains=words[i].title()))
            if query:
                result.extend(query)
    
    thesis1=[]
    thesis2=[]
    output1=[]
    thesis1=[{"faculty_id":thesis1.faculty_id,"thesis_id":thesis1.thesis_id}
    for thesis1 in CommitteeMember.objects.filter(faculty_id=fac_id)]
    if thesis1:
        for i in range(len(thesis1)):
            output1=[{"thesis_id":output1.thesis_id,"title":output1.title,"student_id":output1.student_id,"advisor_id":output1.advisor_id,"grade":output1.grade,"type":output1.type,"year":output1.year,"abstract":output1.abstract}
                for output1 in Thesis.objects.filter(thesis_id=thesis1[i].get("thesis_id").thesis_id)]
            thesis2.extend(output1)

        thesis=[]
        output=[]

        for j in range(len(result)):
                output=[{"thesis_id":output.thesis_id,"title":output.title,"student_id":output.student_id,"advisor_id":output.advisor_id,"grade":output.grade,"type":output.type,"year":output.year,"abstract":output.abstract}
                for output in Thesis.objects.filter(thesis_id=result[j].thesis_id)]
                if output[0] in thesis2 and output[0] not in thesis:
                    thesis.extend(output)
                    output.clear()
                else:
                    output.clear()
    
        if len(thesis)!=0:
            student_info=[]
            advisor_info=[]
        
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
    
        
        
            return Response({"student":student_info,"advisor":advisor_info,"thesis":thesis},status=status.HTTP_200_OK)
        else:
            return Response({"message":"No thesis found"},status=status.HTTP_404_NOT_FOUND)
         
    else:
        return Response({"message":"No thesis found"},status=status.HTTP_404_NOT_FOUND)           

##API to get comments on the thesis based on id of thesis
@api_view(['POST'])
def get_comments(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    id=request.data.get("thesis_id")
    comments=[{"thesis_id":comments.thesis_id,"faculty_id":comments.faculty_id,"comment":comments.comment,"time":comments.time}
                for comments in Comment.objects.filter(thesis_id=id)]
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
        return Response({"message":"No comments for this thesis"},status=status.HTTP_404_NOT_FOUND)

##gets thesis id and logged in faculty member's id and returns the comments made by the logged in faculty member on that thesis                 
@api_view(["POST"])
def get_required_comments(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    thesis_id=request.data.get("thesis_id")
    comments=[{"id":comments.id,"comment":comments.comment,"time":comments.time,"faculty_id":comments.faculty_id,"thesis_id":comments.thesis_id}
    for comments in Comment.objects.filter(thesis_id=thesis_id).filter(faculty_id=fac_id)]

    if len(comments)==0:
        return Response({"No comments found"},status=status.HTTP_404_NOT_FOUND)
    else:
        for i in range(len(comments)):
            comments[i].pop("faculty_id")
            comments[i].pop("thesis_id")
    return Response({"comments":comments},status=status.HTTP_200_OK)

#Add comment
@api_view(['POST'])
def add_comment(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    thesis_id=request.data.get("thesis_id")
    if request.data.get("comment"):
        time=datetime.time(datetime.now()).strftime("%H:%M:%S") 
        serializer=CommentSerializer(data={"faculty_id":fac_id,"thesis_id":thesis_id,"comment":request.data.get("comment"),"time":time})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Comment saved"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Comment not saved"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Please enter comment"},status=status.HTTP_400_BAD_REQUEST)
     
#Delete comment
@api_view(['DELETE'])
def delete_comment(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    id=request.data.get("comment_id")
    comment=Comment.objects.filter(id=id)
    if fac_id!=comment[0].faculty_id.faculty_id:
         return Response({"message":"You can not delete this comment"},status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response({"message":"Comment deleted successfully"},status=status.HTTP_200_OK)

##Edit Thesis
@api_view(['PATCH'])
def edit_thesis(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    thesis_id=request.data.get("thesis_id")
    if request.data.get("grade"):
        g=request.data.get("grade")
        grade=g.title()
    if request.data.get("abstract"):
        abstract=request.data.get("abstract")
    
    thesis= Thesis.objects.get(thesis_id=thesis_id)
    serializer=ThesisSerializer(thesis,data={"grade":grade,"abstract":abstract},partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Thesis edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Thesis not edited"},status=status.HTTP_400_BAD_REQUEST)


#Edit comment
@api_view(['PATCH'])
def edit_comment(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    comment_id=request.data.get("comment_id")
    new_comment=request.data.get("comment")
    comment=Comment.objects.get(id=comment_id)
    time=datetime.time(datetime.now()).strftime("%H:%M:%S") 
    serializer=CommentSerializer(comment,data={"comment":new_comment,"time":time},partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Comment edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Comment edit unsucessful!"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_all_names(request):
    fac=[{"name":fac.name}
    for fac in Faculty.objects.filter()]
    faculty=[]
    for i in range(len(fac)):
        faculty.append(fac[i].get("name"))
    return Response(faculty,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_all_topics(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    required_topics=[{"topic":required_topics.topic,"description":required_topics.description}
    for required_topics in Suggested_topics.objects.filter(faculty_id=fac_id)]

    if len(required_topics)==0:
        return Response({"message":"No topics found"},status=status.HTTP_204_NO_CONTENT)
    else:
        print(required_topics)
        return Response({"result":required_topics},status=status.HTTP_200_OK)

@api_view(["POST"])
def add_topic(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topic=request.data.get("topic")
    if request.data.get("description"):
        description=request.data.get("description")
    else:
        description=None
    serializer=SugestedTopicsSerializer(data={"faculty_id":fac_id,"topic":topic,"description":description})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Topic added successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Topic not added"},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_topic(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topic_id=request.data.get("topic_id")
    required_topic=Suggested_topics.objects.filter(id=topic_id)
    required_topic.delete()
    return Response({"message":"Topic deleted successfully"},status=status.HTTP_200_OK)

@api_view(["PATCH"])
def edit_topic(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topic_id=request.data.get("topic_id")
    
    required_topic=Suggested_topics.objects.get(id=topic_id)
    serializer=SugestedTopicsSerializer(required_topic,data={"topic":request.data.get("new_topic"),"description":request.data.get("description")},partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"Topic edited successfully"},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Topic not edited"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_user_topics(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topics=[{"id":topics.id,"faculty_id":topics.faculty_id,"topic":topics.topic,"description":topics.description}
    for topics in Suggested_topics.objects.filter(faculty_id=fac_id)]
    if len(topics)==0:
        return Response({"message":"No topics found"},status=status.HTTP_404_NOT_FOUND)
    for i in range(len(topics)):
        topics[i].pop("faculty_id")
    return Response({"topics":topics},status=status.HTTP_200_OK)

@api_view(["POST"])
def get_topic_details(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topic_id=request.data.get("topic_id")
    topic=[{"id":topic.id,"topic":topic.topic,"description":topic.description}
    for topic in Suggested_topics.objects.filter(id=topic_id)]
    return Response({"topic":topic},status=status.HTTP_200_OK)

@api_view(["POST"])
##The logged in faculty member can search a particular topic from the list of his own uploaded topics
def search_suggested_topic_faculty(request):
    try:
        if request.session["token"]:
            fac_id=request.session["id"]
    except:
        return Response({"message":"User not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    topic=request.data.get("topic")
    words=topic.split(" ")
    result=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Suggested_topics.objects.filter(Q(topic__icontains=words[i].title()))
            if query:
                result.extend(query)
    
    topics=[]
    for j in range(len(result)):
            output=[{"id":output.id,"topic":output.topic,"description":output.description,"faculty_id":output.faculty_id}
            for output in Suggested_topics.objects.filter(id=result[j].id)]
            
            if output[0] not in topics and output[0].get("faculty_id").faculty_id==fac_id:
                topics.extend(output)
                output.clear()
            else:
                output.clear()
    for i in range(len(topics)):
        topics[i].pop("faculty_id")
        
    return Response({"topics":topics},status=status.HTTP_200_OK)