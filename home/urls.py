from django.urls import path

from . import views
from apps.users.views import user_list

urlpatterns = [
    path("", user_list, name="index_users"),
]
