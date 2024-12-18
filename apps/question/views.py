from rest_framework import viewsets
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Question, Level, Answer, PromptSetting
from apps.users.views import FirebaseAuthentication, IsAuthenticated
from .serializers import (
    LevelSerializer,
    QuestionSerializer,
    AnswerSerializer,
    QuestionWithAnswerSerializer,
)


@login_required(login_url="/users/signin/")
def question_list(request):
    questions = Question.objects.all().order_by("-id")

    page = request.GET.get("page", 1)
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)

    levels = Level.objects.all().order_by("id")
    option_fields = ["option1", "option2", "option3", "option4"]
    return render(
        request,
        "apps/questions.html",
        {"questions": questions, "option_fields": option_fields, "levels": levels},
    )


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


@login_required(login_url="/users/signin/")
def level_list(request):
    levels = Level.objects.all().order_by("-id")

    page = request.GET.get("page", 1)
    paginator = Paginator(levels, 10)
    levels = paginator.page(page)

    return render(request, "apps/levels.html", {"levels": levels})


@login_required(login_url="/users/signin/")
def create_level(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get(
            "image"
        )  # Get the uploaded image file from the request

        # Simple validation to ensure title is not empty
        if title:
            # Create the Level object with title, description, and image
            Level.objects.create(title=title, description=description, image=image)
            return redirect("level_list")  # Redirect to the list view after creation

    return render(request, "create_level.html")


@login_required(login_url="/users/signin/")
def delete_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    level.delete()
    return redirect("level_list")


@login_required(login_url="/users/signin/")
def update_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get(
            "image"
        )  # Get the uploaded image file from the request

        # Update the level fields
        if title:
            level.title = title
        if description:
            level.description = description
        if image:
            level.image = image  # Update the image if a new one is uploaded

        level.save()  # Save the updated level
        return redirect("level_list")  # Redirect to the list view after updating

    return render(request, "update_level.html", {"level": level})


@login_required(login_url="/users/signin/")
def create_question(request):
    if request.method == "POST":
        question_text = request.POST.get("question_text")
        level = request.POST.get("level")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")

        # Create and save the Question object
        Question.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            level_id=level,
        )

        return redirect("question_list")  # Redirect to a list view or success page

    return render(request, "apps/questions.html")  # Adjust to


@login_required(login_url="/users/signin/")
def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect("question_list")


@login_required(login_url="/users/signin/")
def update_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        question.question_text = request.POST.get("question_text")
        question.option1 = request.POST.get("option1")
        question.option2 = request.POST.get("option2")
        question.option3 = request.POST.get("option3")
        question.option4 = request.POST.get("option4")
        question.level = Level.objects.get(id=request.POST.get("level"))
        question.save()
        return redirect("question_list")  # Replace with your success or list URL

    return render(request, "your_template_name.html", {"question": question})


@login_required(login_url="/users/signin/")
def answer_list(request):
    answers = Answer.objects.all().order_by("-id")

    page = request.GET.get("page", 1)
    paginator = Paginator(answers, 10)
    answers = paginator.page(page)

    return render(request, "apps/answers.html", {"answers": answers})


@login_required(login_url="/users/signin/")
def delete_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    answer.delete()
    return redirect("answer_list")


class LevelViewSet(ReadOnlyModelViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.order_by("id")
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_profile = (
            request.user.profile
        )  # Assuming user has a profile with completed answers
        levels = self.get_queryset()
        level_data = []

        for level in levels:
            # Count total questions and answered questions for this level
            total_questions = level.questions_count
            answered_questions_count = Answer.objects.filter(
                profile=user_profile, question__level=level
            ).count()
            completed = False
            if answered_questions_count == 0:
                completed = False
            else:
                # Determine if the level is completed
                completed = answered_questions_count >= total_questions
            serialized_level = self.get_serializer(level).data
            serialized_level["completed"] = completed  # Add the completed flag
            level_data.append(serialized_level)

        return Response(level_data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return QuestionWithAnswerSerializer
        return QuestionSerializer

    def list(self, request, *args, **kwargs):
        user_profile = request.user.profile
        current_level_id = user_profile.level  # Get the user's current level ID

        # Filter the queryset within the list method
        current_level_questions = self.queryset.filter(level_id=current_level_id)
        serializer = self.get_serializer(
            current_level_questions, many=True, context={"profile": user_profile}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer

    # Apply Firebase authentication and require authentication for this viewset
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter answers to show only those associated with the authenticated user's profile
        return Answer.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        from apps.users.models import Profile

        # Automatically set the profile to the user's profile on create
        profile = Profile.objects.get(user=self.request.user)

        # check if answer already exists, if so update the selected_option
        answer = Answer.objects.filter(
            question=serializer.validated_data["question"], profile=profile
        ).first()

        serializer.validated_data["profile"] = profile

        # if there was selected-option, then make sure you're setting
        # the skipped field to False
        if (
            "selected_option" in serializer.validated_data
            and serializer.validated_data["selected_option"]
        ):
            serializer.validated_data["skipped"] = False
            serializer.validated_data["selected_option_text"] = getattr(
                serializer.validated_data["question"],
                "option" + serializer.validated_data["selected_option"],
            )

        # if the skipped field is set to True, then set the selected_option to None
        if serializer.validated_data["skipped"]:
            serializer.validated_data["selected_option"] = None
            serializer.validated_data["selected_option_text"] = None

        if answer:
            # Update existing answer instead of creating a new one
            answer.selected_option = serializer.validated_data.get("selected_option")
            answer.selected_option_text = serializer.validated_data.get(
                "selected_option_text"
            )
            answer.skipped = serializer.validated_data.get("skipped", answer.skipped)
            answer.save()
        else:
            serializer.save()

    def perform_update(self, serializer):
        from apps.users.models import Profile

        # Automatically set the profile to the user's profile on update
        profile = Profile.objects.get(user=self.request.user)
        serializer.validated_data["profile"] = profile

        # if there was selected-option, then make sure you're setting
        # the skipped field to False
        if (
            "selected_option" in serializer.validated_data
            and serializer.validated_data["selected_option"]
        ):
            serializer.validated_data["skipped"] = False
            serializer.validated_data["selected_option_text"] = getattr(
                serializer.validated_data["question"],
                "option" + serializer.validated_data["selected_option"],
            )

        # if the skipped field is set to True, then set the selected_option to None
        if serializer.validated_data["skipped"]:
            serializer.validated_data["selected_option"] = None
            serializer.validated_data["selected_option_text"] = None

        serializer.save()
