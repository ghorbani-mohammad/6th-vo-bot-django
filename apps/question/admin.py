from django.contrib import admin

from . import models


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

