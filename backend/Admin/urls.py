from django.urls import path,include

from Thesis.views import *
from Admin.views import *
urlpatterns=[
   

    path("login/", login_admin),
    path("logout/", logout_admin),
    path("thesis-view/",thesis_view),
    path("edit-thesis/", thesis_edit),
    path("register-student/", register_student),
    path("register-faculty/", register_faculty),
    path("view-students/", view_students),
    path("view-faculty/", view_faculty),
    path("edit-faculty/", edit_faculty),
    path("edit-student/", edit_student),
    path("delete-faculty/<int:id>/", delete_faculty),
    path("delete-student/<int:id>/", delete_student),
    path("view-comments/", view_comments),
    path("change-password/", change_password),
    path("view-faculty-detail/",view_faculty_detail),
    path("view-student-detail/",view_student_detail),
    path("upload-thesis/",upload_thesis),
    path("search-student/",search_student_list),
    path("search-faculty/",search_faculty_list),
    path("add-domain/",add_domain),
]