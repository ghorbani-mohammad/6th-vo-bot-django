import uuid
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import ProductSerializer
from apps.common.models import Product
from apps.users.views import FirebaseAuthentication
from apps.users.models import Profile
from apps.question.models import PromptSetting, HoroscopeLog, Todo
from apps.question.serializers import TodoSerializer
from apps.utils.ai_bot import generate_horoscope, generate_todos


class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user and request.user.is_authenticated


@api_view(["GET"])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def profile_horoscopy(request):
    profile = get_object_or_404(Profile, user=request.user)
    cache_key = f"horoscope_{profile.user.id}"
    cached_horoscopes = cache.get(cache_key)

    # Return cached horoscopes if available
    if cached_horoscopes:
        return JsonResponse(cached_horoscopes)

    if not profile.answered_questions_count:
        return Response(
            {
                "personal_growth": "Please answer some questions to get your horoscope",
                "success": "Please answer some questions to get your horoscope",
                "relationship": "Please answer some questions to get your horoscope",
            }
        )

    # get five random question and answer from user
    questions = profile.answered_questions.order_by("?")[
        : min(10, profile.answered_questions_count)
    ]
    user_personality = ""
    for question in questions:
        user_personality += f"Q: {question.question_text}\nA: {question.profile_answer(profile).selected_option_text}\n"

    prompts_setting = PromptSetting.objects.filter(is_active=True).last()

    prompts = {
        "personal_growth": prompts_setting.personal_growth,
        "success": prompts_setting.success,
        "relationship": prompts_setting.relationships,
    }

    horoscopes = generate_horoscope(
        user_personality,
        prompts,
        prompts_setting.temperature,
        prompts_setting.max_tokens,
    )
    cache.set(cache_key, horoscopes, timeout=prompts_setting.cache_duration)
    HoroscopeLog.objects.create(
        profile=profile,
        horoscope=f"user_personality:{user_personality}\nhoroscope:{horoscopes}",
    )
    return Response(horoscopes)


@api_view(["GET"])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def profile_suggestions(request):
    profile = get_object_or_404(Profile, user=request.user)
    cache_key = f"profile_suggestions_{profile.user.id}"
    cached_horoscopes = cache.get(cache_key)

    # Return cached horoscopes if available
    if cached_horoscopes:
        result = cached_horoscopes
        todo_id = result.get("todos_id")
        if todo_id:
            todos = Todo.objects.get(random_id=todo_id)
            cached_horoscopes["personal_growth_checked"] = todos.personal_growth_checked
            cached_horoscopes["success_checked"] = todos.success_checked
            cached_horoscopes["relationships_checked"] = todos.relationships_checked
        return JsonResponse(cached_horoscopes)

    if not profile.answered_questions_count:
        return Response(
            {
                "personal_growth": "Please answer some questions to get your horoscope",
                "personal_growth_todo": "Please answer some questions to get your todo for personal growth",
                "success": "Please answer some questions to get your horoscope",
                "success_todo": "Please answer some questions to get your todo for success",
                "relationship": "Please answer some questions to get your horoscope",
                "relationship_todo": "Please answer some questions to get your todo for relationship",
                "affirmation": "Please answer some questions to get your horoscope",
                "thinker": "Please answer some questions to get your horoscope",
                "quote": "Please answer some questions to get your horoscope",
            }
        )

    # get five random question and answer from user
    questions = profile.answered_questions.order_by("?")[
        : min(10, profile.answered_questions_count)
    ]
    user_personality = ""
    for question in questions:
        user_personality += f"Q: {question.question_text}\nA: {question.profile_answer(profile).selected_option_text}\n"

    prompts_setting = PromptSetting.objects.filter(is_active=True).last()

    horoscope_prompts = {
        "personal_growth": prompts_setting.personal_growth,
        "success": prompts_setting.success,
        "relationship": prompts_setting.relationships,
        "affirmation": prompts_setting.affirmation,
        "thinker": prompts_setting.thinker,
        "quote": prompts_setting.quote,
    }

    horoscopes = generate_horoscope(
        user_personality,
        horoscope_prompts,
        prompts_setting.temperature,
        prompts_setting.max_tokens,
    )

    todo_prompts = {
        "personal_growth_todo": prompts_setting.personal_growth_todo,
        "success_todo": prompts_setting.success_todo,
        "relationship_todo": prompts_setting.relationships_todo,
    }

    todos = generate_todos(
        user_personality,
        todo_prompts,
        prompts_setting.temperature,
        prompts_setting.max_tokens,
    )

    # combine horoscopes and todos
    combined_result = {**horoscopes, **todos}
    todos_id = uuid.uuid4()
    combined_result["todos_id"] = todos_id
    Todo.objects.create(
        random_id=todos_id,
        profile=profile,
        todos=todos,
    )

    cache.set(cache_key, combined_result, timeout=prompts_setting.cache_duration)
    HoroscopeLog.objects.create(
        profile=profile,
        horoscope=f"user_personality:{user_personality}\nhoroscope:{horoscopes}\ntodo:{todos}",
    )
    return Response(combined_result)


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'random_id'
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        # Optionally filter todos by profile if needed
        return self.queryset.filter(profile=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
