from django.urls import path

from . import views

urlpatterns = [
    path("prompts_setting/", views.prompts_setting, name="prompts_setting"),
    path(
        "update_prompts_setting/",
        views.update_prompts_setting,
        name="update_prompts_setting",
    ),
]
