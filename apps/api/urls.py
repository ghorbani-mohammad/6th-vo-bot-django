from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views import profile_horoscopy, profile_suggestions, TodoViewSet
from apps.users.views import firebase_login, profile_info, delete_account
from apps.question.views import LevelViewSet, QuestionViewSet, AnswerViewSet


router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r"content/levels", LevelViewSet, basename="level")
router.register(r"content/question", QuestionViewSet, basename="question")
router.register(r"content/answers", AnswerViewSet, basename="answer")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/profile/", profile_info, name="profile_info"),
    path("auth/firebase-login/", firebase_login, name="firebase_login"),
    path("auth/delete-account/", delete_account, name="delete_account"),
    path("horoscopy/", profile_horoscopy, name="profile_horoscopy"),
    path("v2/horoscopy/", profile_suggestions, name="profile_horoscopy_v2"),
]
