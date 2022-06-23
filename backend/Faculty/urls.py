from django.urls import path,include
from Faculty.views import *
urlpatterns=[
  
    
    path("login/",login_faculty),
    path("logout/",faculty_logout),
    path("evaluated-thesis/",show_evaluated_thesis),
    path("supervised-thesis/",show_supervided_thesis),
    path("view-thesis/",view_thesis),
    path("search-supervised-thesis/",search_by_topic_supervised_thesis),
    path("search-evaluated-thesis/",search_by_topic_evaluated_thesis),
    path("show-comments/",get_comments),
    path("add-comment/",add_comment),
    path("edit-thesis/",edit_thesis),
    path("edit-comment/",edit_comment),
    path("delete-comment/",delete_comment),
    path("get-comments/",get_required_comments),
    path("get-all-names/",get_all_names),
    path("all-topics/",get_all_topics),
    path("add-topic/",add_topic),
    path("delete-topic/",delete_topic),
    path("edit-topic/",edit_topic),
    path("get-user-topics/",get_user_topics),
    path("get-topic-details/",get_topic_details),
    path("search-suggested-topic/",search_suggested_topic_faculty)
]