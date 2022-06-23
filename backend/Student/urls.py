from django.urls import path,include
from Student.views import *

urlpatterns=[
    path("login/",login_student),
    path("logout/",student_logout),
    path("upload-thesis/",upload_thesis),
    path("edit-thesis/",edit_thesis),
]