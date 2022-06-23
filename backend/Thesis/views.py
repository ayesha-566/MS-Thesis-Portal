from ast import Return
from functools import partial
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from Thesis.models import Thesis,Domain,DomainInfo,DomainFreq, DomainsTrend, Conference
from Student.models import Student
from Faculty.models import Faculty
from rest_framework.response import Response
from Student.serializers import StudentSerializer
from Faculty.serializers import FacultySerializer
from Thesis.serializers import ConferenceSerializer
from Faculty.models import Suggested_topics
from Admin.models import Admin
from django.db.models import Q
import datetime
import requests
from bs4 import BeautifulSoup
import random
import datetime


@api_view(["POST"])
def search_thesis(request):
      output=[]

      if request.data.get("rollno"):
            rollnum=request.data.get("rollno")
            rollnum=rollnum.upper() 
            student=[{"rollno":student.rollno,"student_id":student.student_id}
            for student in Student.objects.filter(rollno=rollnum)]

            if student:
             std_id=student[0].get("student_id")
             thesis_output=[{"thesis_id":thesis_output.thesis_id}
             for thesis_output in Thesis.objects.filter(student_id=std_id)]
 
             if len(thesis_output)==0:
                   return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
             
             else:
                  temp=[]
                  for obj in thesis_output:
                        id=obj.get("thesis_id")
                        temp.append(id)
                        obj.pop("thesis_id")

                  thesis_output=temp

                  if len(output)==0:
                         output.extend(thesis_output)
                  else:
                         output=list(set(output).intersection(thesis_output))
                         if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
            else:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

      if request.data.get("author"):
            name=request.data.get("author")
            words=name.split(" ")
            result=[]

            for i in range(len(words)):
                  if words[i]!=" ":
                        query=Student.objects.filter(Q(name__icontains=words[i].title()))
                        if query:
                              result.extend(query)
            
            output_temp=[]
            thesis_output=[]

            for i in range(len(result)):
                  output_temp=[{"thesis_id":output_temp.thesis_id}
                  for output_temp in Thesis.objects.filter(student_id=result[i].student_id)]
                  if output_temp:
                        if output_temp not in thesis_output:
                              thesis_output.extend(output_temp)
                              output_temp.clear()
                  
                        else:
                              output_temp.clear()       

            if len(thesis_output)==0:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
             
            else:
                  temp=[]
                  for obj in thesis_output:
                        id=obj.get("thesis_id")
                        temp.append(id)
                        obj.pop("thesis_id")
                        
                  thesis_output=temp

                  if len(output)==0:
                        output.extend(thesis_output)
                  else:
                        output=list(set(output).intersection(thesis_output))
                        if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

      if request.data.get("advisor"):
            name=request.data.get("advisor")
            words=name.split(" ")
            result=[]

            for i in range(len(words)):
                  if words[i]!=" ":
                        query=Faculty.objects.filter(Q(name__icontains=words[i].title()))
                        if query:
                              result.extend(query)

            output_temp=[]
            thesis_output=[]

            for i in range(len(result)):
                  output_temp=[{"thesis_id":output_temp.thesis_id}
                  for output_temp in Thesis.objects.filter(advisor_id=result[i].faculty_id)]
                  if output_temp:
                        if output_temp not in thesis_output:
                              thesis_output.extend(output_temp)
                              output_temp.clear()
                  
                        else:
                              output_temp.clear()

            if len(thesis_output)==0:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
             
            else:
                  temp=[]
                  for obj in thesis_output:
                        id=obj.get("thesis_id")
                        temp.append(id)
                        obj.pop("thesis_id")
                        
                  thesis_output=temp

                  if len(output)==0:
                        output.extend(thesis_output)
                  else:
                        output=list(set(output).intersection(thesis_output))
                        if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)  

      if request.data.get("year"):
            
            thesis_output=[{"thesis_id":thesis_output.thesis_id}
            for thesis_output in Thesis.objects.filter(year=request.data.get("year"))]

            if len(thesis_output)==0:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

            else:
                  temp=[]
                  for obj in thesis_output:
                        id=obj.get("thesis_id")
                        temp.append(id)
                        obj.pop("thesis_id")

                  thesis_output=temp

                  if len(output)==0:
                         output.extend(thesis_output)
                  else:
                         output=list(set(output).intersection(thesis_output))
                         if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
      
      if request.data.get("title"):
            title_thesis=request.data.get("title")
            title_thesis=title_thesis.title() 

            words=title_thesis.split(" ")
            thesis_output=[]
            output_temp=[]
            result=[]

            for i in range(len(words)):
                  if words[i]!=" ":
                        query=Thesis.objects.filter(Q(title__icontains=words[i].title()))
                        if query:
                              result.extend(query)
                      
            if len(result)==0:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
             
            else:
                  temp=[]
                  for j in range(len(result)):
                        temp.append(result[j].thesis_id)
                  
                  thesis_output=temp

                  if len(output)==0:
                        output.extend(thesis_output)
                  else:
                        output=list(set(output).intersection(thesis_output))
                        if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

      if request.data.get("domain"):
            domains=request.data.get("domain")
            
            domain_list=[]
            for object in domains:
                  domain=[{"domain_id":domain.domain_id}
                  for domain in Domain.objects.filter(name=object)]
                  domain_list.extend(domain)
            
            temp=[]
            for object in domain_list:
                  id=object.get("domain_id")
                  print(id)
                  temp.append(id)
                  object.pop("domain_id")
            
            domain_list=temp
         
            if len(domain_list)!=0:
             thesis_output=[]
             for object in domain_list:
                  thesis_output1=[{"thesis_id":thesis_output1.thesis_id}
                  for thesis_output1 in DomainInfo.objects.filter(domain_id=object)]

                  if len(thesis_output1)==0:
                   return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

                  else:
                        temp=[]
                        for obj in thesis_output1:
                              id=obj.get("thesis_id").thesis_id
                              temp.append(id)
                              obj.pop("thesis_id")
                        
                        thesis_output1=temp

                        if len(thesis_output)==0:
                              thesis_output.extend(thesis_output1)
                        else:
                              thesis_output=list(set(thesis_output).intersection(thesis_output1))
                              if len(thesis_output)==0:
                                    return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

             if len(thesis_output)==0:
                   return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
             
             else:
                   if len(output)==0:
                         output.extend(thesis_output)
                   else:
                         output=list(set(output).intersection(thesis_output))
                         if len(output)==0:
                               return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)
            else:
                  return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

      if len(output)==0:
            return Response({"message":"No results!"},status=status.HTTP_204_NO_CONTENT)

      student_info=[]
      advisor_info=[]
      domain_info=[]
      thesis_info=[]

      for object in output:
            thesis_output=[{"thesis_id":thesis_output.thesis_id,"title":thesis_output.title, "student_id":thesis_output.student_id, "advisor_id":thesis_output.advisor_id, "type":thesis_output.type,"year":thesis_output.year}
            for thesis_output in Thesis.objects.filter(thesis_id=object)]
            thesis_info.extend(thesis_output)
      
      for object in thesis_info:
            std=object.get("student_id")
            student=[{"name":student.name,"rollno":student.rollno}
            for student in Student.objects.filter(student_id=std.student_id)]
            student_info.extend(student)
            object.pop("student_id")
     
      for object in thesis_info:
            adv=object.get("advisor_id")
            advisor=[{"name":advisor.name}
            for advisor in Faculty.objects.filter(faculty_id=adv.faculty_id)]
            advisor_info.extend(advisor)
            object.pop("advisor_id")

      for object in thesis_info:
            thesis_id=object.get("thesis_id")  
            domain=[{"domain_id": domain.domain_id}
            for domain in DomainInfo.objects.filter(thesis_id=thesis_id)]
            temp=[]
            for obj in domain:
                              id=obj.get("domain_id").domain_id
                              temp.append(id)
                              obj.pop("domain_id")

            domains=[]
            for obj in temp:
                  domain=[{"name":domain.name}
                  for domain in Domain.objects.filter(domain_id=obj)]
                  for obj2 in domain:
                        dom_name=obj2.get("name")
                        domains.append(dom_name)
                        domains.append(", ")
                        obj2.pop("name")
                  
            domains=domains[:-1]      
            domain_info.append(domains)

      return Response({"student":student_info,"advisor":advisor_info,"domains":domain_info,"thesis":thesis_info},status=status.HTTP_200_OK)

@api_view(['POST'])
def show_thesis_public(request):
      thesis=[{"thesis_id":thesis.thesis_id,"title":thesis.title,"student_id":thesis.student_id,"advisor_id":thesis.advisor_id,"grade":thesis.grade,"type":thesis.type,"year":thesis.year,"abstract":thesis.abstract,"future_work":thesis.future_work}
                        for thesis in Thesis.objects.filter(thesis_id=request.data.get("thesis_id"))]
      
      student_info=[]
      advisor_info=[]
      domains=[]
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
          object2.pop("grade")
          

      for object3 in thesis:
          id=object3.get("thesis_id")
          domain_info=[{"thesis_id":domain_info.thesis_id,"domain_id":domain_info.domain_id}
          for domain_info in DomainInfo.objects.filter(thesis_id=id)]
          domain=domain_info[0].get("domain_id")
          dom_id=domain.domain_id
          dom_names=[{"name":dom_names.name}
          for dom_names in Domain.objects.filter(domain_id=dom_id)]
          domains.extend(dom_names)

        
      return Response({"student":student_info,"advisor":advisor_info,"domains":domains,"thesis":thesis},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_random_thesis(request):
    theses=Thesis.objects.all()
    if len(theses)>4:
        max_id = Thesis.objects.filter().order_by('thesis_id').last().thesis_id
        min_id=Thesis.objects.filter().order_by('thesis_id').first().thesis_id
        random_num=random.sample(range(min_id,max_id),4)
        thesis=[]
        output=[]
        for i in range(4):
                output=[{"thesis_id":output.thesis_id,"title":output.title,"student_id":output.student_id,"advisor_id":output.advisor_id,"grade":output.grade,"type":output.type,"year":output.year,"abstract":output.abstract}
                for output in Thesis.objects.filter(thesis_id=random_num[i])]
                thesis.extend(output)
                output.clear()
    if len(theses)<=4:
        thesis=[]
        output=[]
        for i in range(len(theses)):
                output=[{"thesis_id":output.thesis_id,"title":output.title,"student_id":output.student_id,"advisor_id":output.advisor_id,"grade":output.grade,"type":output.type,"year":output.year,"abstract":output.abstract}
                for output in Thesis.objects.filter(thesis_id=theses[i].thesis_id)]
                thesis.extend(output)
                output.clear()
   
    student_info=[]
    advisor_info=[]
    domain_info=[]
     
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
          object2.pop("grade")
          object2.pop("abstract")
         
    for object in thesis:
            thesis_id=object.get("thesis_id")  
            domain=[{"domain_id": domain.domain_id}
            for domain in DomainInfo.objects.filter(thesis_id=thesis_id)]
            temp=[]
            for obj in domain:
                              id=obj.get("domain_id").domain_id
                              temp.append(id)
                              obj.pop("domain_id")
            domains=[]
            for obj in temp:
                  domain=[{"name":domain.name}
                  for domain in Domain.objects.filter(domain_id=obj)]
                  for obj2 in domain:
                              dom_name=obj2.get("name")
                              domains.append(dom_name)
                              domains.append(", ")
                              obj2.pop("name")
            domains=domains[:-1]
            domain_info.append(domains)
       
    return Response({"student":student_info,"advisor":advisor_info,"thesis":thesis, "domains":domain_info},status=status.HTTP_200_OK)

@api_view(['GET'])
def view_graphs(request):

    graph1=[{"name":graph1.name,"frequency":graph1.frequency}
            for graph1 in DomainFreq.objects.raw('SELECT "Thesis_domain".name, COUNT("Thesis_domain".name) AS frequency '
            'FROM "Thesis_domain" JOIN "Thesis_domaininfo" ON "Thesis_domain".domain_id = "Thesis_domaininfo".domain_id_id '
            'GROUP BY "Thesis_domain".name ORDER BY frequency DESC LIMIT 5')]
    
    graph2=[{"year":graph2.year, "name":graph2.name,"frequency":graph2.frequency}
            for graph2 in DomainsTrend.objects.raw('SELECT "year", "name", COUNT(*) AS frequency ' 
            'FROM ("Thesis_domaininfo" JOIN "Thesis_thesis" ON "Thesis_domaininfo".thesis_id_id="Thesis_thesis".thesis_id) ' 
            'JOIN "Thesis_domain" ON "Thesis_domaininfo".domain_id_id="Thesis_domain".domain_id ' 
            'WHERE "name" IN (SELECT domain_names FROM (SELECT "Thesis_domain".name AS domain_names, COUNT("Thesis_domain".name) AS frequency '
            'FROM "Thesis_domain" JOIN "Thesis_domaininfo" ON "Thesis_domain".domain_id = "Thesis_domaininfo".domain_id_id '
            'GROUP BY "Thesis_domain".name ORDER BY frequency DESC LIMIT 5) AS domains_table) GROUP BY "name", "year" '
            'HAVING "year" >= (EXTRACT(YEAR FROM CURRENT_DATE) - 3) and "year" <= EXTRACT(YEAR FROM CURRENT_DATE) ORDER BY "year" DESC')]

    return Response({"graph1":graph1, "graph2":graph2},status=status.HTTP_200_OK)

@api_view(['GET'])
def all_suggested_topics(request):
    required_topics=[{"topic":required_topics.topic,"description":required_topics.description,"faculty_id":required_topics.faculty_id}
    for required_topics in Suggested_topics.objects.filter()]
    
    if len(required_topics)==0:
        return Response({"message":"No topics found"},status=status.HTTP_404_NOT_FOUND)
    else:
         faculty=[]
         output2=[]
    
         for k in range(len(required_topics)):
            output2=[{"name":output2.name}
            for output2 in Faculty.objects.filter(faculty_id=required_topics[k].get("faculty_id").faculty_id)]
            faculty.extend(output2)
            required_topics[k].pop("faculty_id")
            output2.clear()
         
         return Response({"topics":required_topics,"faculty":faculty},status=status.HTTP_200_OK)

@api_view(["GET"])
def get_all_domains(request):
    dom=[{"name":dom.name}
    for dom in Domain.objects.filter()]
    domains=[]
    for i in range(len(dom)):
        domains.append(dom[i].get("name"))
    return Response({"domains":domains},status=status.HTTP_200_OK)

@api_view(["POST"])
def search_suggested_topics(request):
    topic=request.data.get("title")
    words=topic.split(" ")
    result=[]
    topics=[]
    output=[]

    for i in range(len(words)):
        if words[i]!=" ":
            query=Suggested_topics.objects.filter(Q(topic__icontains=words[i].title()))
            if query:
                result.extend(query)
    
    if len(result)==0:
        return Response({"message":"No topics found"},status=status.HTTP_404_NOT_FOUND)


    for j in range(len(result)):
                output=[{"id":output.id,"topic":output.topic,"faculty_id":output.faculty_id,"description":output.description}
                for output in Suggested_topics.objects.filter(id=result[j].id)]
                if output[0] not in topics:
                    topics.extend(output)
                    output.clear()
                else:
                    output.clear()

    faculty=[]
    output2=[]
    
    for k in range(len(topics)):
        output2=[{"name":output2.name}
        for output2 in Faculty.objects.filter(faculty_id=topics[k].get("faculty_id").faculty_id)]
        faculty.extend(output2)
        topics[k].pop("faculty_id")
        output2.clear()

    return Response({"topics":topics,"faculty":faculty},status=status.HTTP_200_OK)

@api_view(["GET"])
def get_name(request):
    username=request.session["username"]
    faculty=[{"name":faculty.name}
    for faculty in Faculty.objects.filter(username=username)]
    if faculty:
        name=faculty[0].get("name")
        return Response(name,status=status.HTTP_200_OK) 
        
    else:
        admin=[{"name":admin.name}
        for admin in Admin.objects.filter(username=username)]
        if admin:
            name=admin[0].get("name")
            return Response(name,status=status.HTTP_200_OK)
        else:
            student=[{"name":student.name}
            for student in Student.objects.filter(email=username)]
            name=student[0].get("name")
            return Response(name,status=status.HTTP_200_OK)

@api_view(["GET"])
def check_admin_session(request):
    try:
        if request.session["token"]:
            id=request.session["id"]
            username=request.session["username"]
            if Admin.objects.filter(admin_id=id).filter(username=username):
                return Response({"message":"Admin logged in"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Admin not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"message":"Admin not logged in"},status=status.HTTP_401_UNAUTHORIZED)

    
@api_view(["GET"])
def check_faculty_session(request):
    try:
        if request.session["token"]:
            id=request.session["id"]
            username=request.session["username"]
            if Faculty.objects.filter(faculty_id=id).filter(username=username):
                return Response({"message":"Faculty logged in"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Faculty not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"message":"Faculty not logged in"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def check_student_session(request):
    try:
        if request.session["token"]:
            id=request.session["id"]
            username=request.session["username"]
            if Student.objects.filter(student_id=id).filter(email=username):
                return Response({"message":"Student logged in"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Student not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"message":"Student not logged in"},status=status.HTTP_401_UNAUTHORIZED)

#Crawler 
@api_view(["GET"])
def get_data_from_web(request):
        count=Conference.objects.count()
        if count>0:
            Conference.objects.all().delete()
        startURL="https://www.computer.org/publications/tech-news/events/2022-top-computer-science-conferences"
        links=[]
        page=requests.get(startURL)
        soup=BeautifulSoup(page.text,"lxml")
        heading_tags = ["h2", "h3","strong"]
        months2=[]
        venueString=[]
        links=[]
        title=[]
        months=["January","February","March","April","May","June","July","August","September","October","November","December"]
        for tags in soup.find_all(heading_tags):
                if tags.text == "Past Conferences":
                    break
                if tags.text == "Recommended by IEEE Computer Society":
                    break
                if tags.text.strip() in months:
                    month=tags.text.strip()
                if tags.name=="h3":
                    title.append(tags.text.strip())
                    href=tags.contents[0]
                    links.append(href.get("href"))
                    months2.append(month)
                if tags.name=="strong":
                    venueString.append(tags.text.strip())
    
        venueString2=[]
        dates=[]
        venues=[]
        for i in range(len(venueString)):
            line=venueString[i]
            words=line.split(" ")
            for w in words:
                if w in months:
                    venueString2.append(venueString[i])
                    break
        
        for j in range(len(venueString2)):
            words=venueString2[j].split("/")
            venues.append(words[0])
            dates.append(words[1])
        
        for k in range(len(links)):
            serializer=ConferenceSerializer(data={"month":months2[k],"name":title[k],"date":dates[k],"link":links[k],"venue":venues[k]})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"message":"Error"},status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_model_info(response):
    count=Conference.objects.count()
    if count>0:
        conference=Conference.objects.last()
        modified_date=conference.date_modified.strftime('%Y-%m-%d')  
        return Response({"message":"Not empty","date":modified_date},status=status.HTTP_200_OK)
    else:
        return Response({"message":"empty","date":""},status=status.HTTP_200_OK)
  

@api_view(["GET"])
def get_conferences_data(response):
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    month=datetime.datetime.now().month-1
    conferences=[]
    i=0
    while i<4:
        if month+i<=12:
            output1=[{"month":output1.month,"name":output1.name,"date":output1.date,"link":output1.link,"venue":output1.venue}
            for output1 in Conference.objects.filter(month=months[month+i])]
            if output1:
                conferences.extend(output1)
                output1.clear()
            i=i+1
        else:
            break
    return Response({"conferences":conferences},status=status.HTTP_200_OK)

@api_view(["GET"])
def get_all_conferences(request):
    conferences=[{"id":conferences.id,"month":conferences.month,"name":conferences.name,"date":conferences.date,"link":conferences.link,"venue":conferences.venue}
    for conferences in Conference.objects.filter()]
    return Response({"conferences":conferences},status=status.HTTP_200_OK)
