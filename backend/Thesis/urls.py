from urllib.parse import urlparse
from django.urls import URLPattern, path,include
from Thesis.views import *

urlpatterns=[
    path("view-thesis/",show_thesis_public),
    path("search/",search_thesis),
    path("show-thesis/",get_random_thesis),
    path("view-graphs/",view_graphs),
    path("suggested-topics/",all_suggested_topics),
    path("get-domains/",get_all_domains),
    path("search-suggested-topics/",search_suggested_topics),
    path("get-name/",get_name),
    path("check-admin-session/",check_admin_session),
    path("check-faculty-session/",check_faculty_session),
    path("check-student-session/",check_student_session),
    path("get-data-from-web/",get_data_from_web),
    path("get-conferences/",get_conferences_data),
    path("get-model-info/",get_model_info),
    path("get-all-conferences/",get_all_conferences)
]