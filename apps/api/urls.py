from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import profile_info


router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("auth/profile/", profile_info, name="profile_info"),
]
