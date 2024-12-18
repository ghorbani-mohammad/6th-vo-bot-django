from django.contrib import admin

from . import models


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "description", "image", "questions_count"]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["pk", "question_text", "level"]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "question",
        "profile",
        "skipped",
        "selected_option",
        "selected_option_text",
    ]


@admin.register(models.PromptSetting)
class PromptSettingAdmin(admin.ModelAdmin):
    list_display = [
        "personal_growth",
        "success",
        "relationships",
        "is_active",
        "temperature",
        "max_tokens",
    ]


@admin.register(models.HoroscopeLog)
class HoroscopeLogAdmin(admin.ModelAdmin):
    list_display = ["profile", "created_at"]


@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = [
        "random_id",
        "profile",
        "personal_growth_checked",
        "success_checked",
        "relationships_checked",
    ]