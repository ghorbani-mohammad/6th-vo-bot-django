from rest_framework import viewsets
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import PromptSetting
from apps.users.views import FirebaseAuthentication, IsAuthenticated


@login_required(login_url="/users/signin/")
def prompts_setting(request):
    prompts_setting = PromptSetting.objects.filter(is_active=True).last()

    return render(request, "apps/prompts_setting.html", {"setting": prompts_setting})


@login_required(login_url="/users/signin/")
def update_prompts_setting(request):
    prompts_setting = PromptSetting.objects.filter(is_active=True).last()
    if request.method == "POST":
        prompts_setting.personal_growth = request.POST.get("personal_growth")
        prompts_setting.personal_growth_todo = request.POST.get("personal_growth_todo")
        prompts_setting.success = request.POST.get("success")
        prompts_setting.success_todo = request.POST.get("success_todo")
        prompts_setting.relationships = request.POST.get("relationships")
        prompts_setting.relationships_todo = request.POST.get("relationships_todo")
        prompts_setting.affirmation = request.POST.get("affirmation")
        prompts_setting.thinker = request.POST.get("thinker")
        prompts_setting.quote = request.POST.get("quote")
        prompts_setting.temperature = request.POST.get("temperature", 0)
        prompts_setting.max_tokens = request.POST.get("max_tokens", 200)
        prompts_setting.cache_duration = request.POST.get(
            "cache_duration", 24 * 60 * 60
        )
        prompts_setting.save()

        messages.success(request, "Prompts setting updated successfully")

    return render(request, "apps/prompts_setting.html", {"setting": prompts_setting})

