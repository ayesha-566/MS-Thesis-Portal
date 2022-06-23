import requests
from bs4 import BeautifulSoup


def crawler():
    startURL="https://www.computer.org/publications/tech-news/events/2022-top-computer-science-conferences"
    links=[]
    page=requests.get(startURL)
    soup=BeautifulSoup(page.text,"lxml")
    heading_tags = ["h2", "h3","strong"]
    months2=[]
    venueString=[]
    links=[]
    title=[]
    flag=False
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    for tags in soup.find_all(heading_tags):
            if tags.text == "Past Conferences":
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



       
        

            


  