from django.urls import path

from . import views

urlpatterns = [
    path("question/create/", views.create_question, name="create_question"),
    path("question/update/<int:id>/", views.update_question, name="update_question"),
    path("question/delete/<int:id>/", views.delete_question, name="delete_question"),
    path("questions/", views.question_list, name="question_list"),
    path("levels/", views.level_list, name="level_list"),
    path("answers/", views.answer_list, name="answer_list"),
    path("answers/delete/<int:id>/", views.delete_answer, name="delete_answer"),
    path("levels/create/", views.create_level, name="create_level"),
    path("levels/delete/<int:level_id>/", views.delete_level, name="delete_level"),
    path("levels/update/<int:level_id>/", views.update_level, name="update_level"),
    path("prompts_setting/", views.prompts_setting, name="prompts_setting"),
    path(
        "update_prompts_setting/",
        views.update_prompts_setting,
        name="update_prompts_setting",
    ),
]
