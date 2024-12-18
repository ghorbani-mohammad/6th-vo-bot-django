from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import CreateView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth as firebase_auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.common.models import Product
from apps.users.models import Profile
from apps.users.forms import (
    SigninForm,
    SignupForm,
    UserPasswordChangeForm,
    UserSetPasswordForm,
    UserPasswordResetForm,
    ProfileForm,
)
from apps.users.utils import user_filter


class SignInView(LoginView):
    form_class = SigninForm
    template_name = "authentication/sign-in.html"


class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "authentication/sign-up.html"
    success_url = "/users/signin/"


class UserPasswordChangeView(PasswordChangeView):
    template_name = "authentication/password-change.html"
    form_class = UserPasswordChangeForm


class UserPasswordResetView(PasswordResetView):
    template_name = "authentication/forgot-password.html"
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = "authentication/reset-password.html"
    form_class = UserSetPasswordForm


@login_required(login_url="/users/signin/")
def signout_view(request):
    logout(request)
    return redirect(reverse("signin"))


@login_required(login_url="/users/signin/")
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "segment": "profile",
    }
    return render(request, "dashboard/profile.html", context)


@login_required(login_url="/users/signin/")
def upload_avatar(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        profile.avatar = request.FILES.get("avatar")
        profile.save()
        messages.success(request, "Avatar uploaded successfully")
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/signin/")
def change_password(request):
    user = request.user
    if request.method == "POST":
        if check_password(request.POST.get("current_password"), user.password):
            user.set_password(request.POST.get("new_password"))
            user.save()
            messages.success(request, "Password changed successfully")
        else:
            messages.error(request, "Password doesn't match!")
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/signin/")
def user_list(request):
    filters = user_filter(request)
    user_list = User.objects.filter(**filters).select_related("profile").order_by("-id")
    form = SignupForm()

    page = request.GET.get("page", 1)
    paginator = Paginator(user_list, 10)
    users = paginator.page(page)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        "users": users,
        "form": form,
    }
    return render(request, "apps/users.html", context)


@login_required(login_url="/users/signin/")
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/signin/")
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/signin/")
def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.email = request.POST.get("email")
        user.profile.name = request.POST.get("name")
        user.profile.zodiac_sign = request.POST.get("zodiac_sign")
        user.save()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/signin/")
def user_change_password(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.set_password(request.POST.get("password"))
        user.save()
    return redirect(request.META.get("HTTP_REFERER"))


@api_view(["POST"])
@permission_classes([AllowAny])
def firebase_login(request):
    # Get Firebase token from headers or request data
    if "Authorization" in request.headers:
        firebase_token = request.headers.get("Authorization").split().pop()
        print(f"firebase_token: {firebase_token}")

        # Verify token
        decoded_token = firebase_auth.verify_id_token(firebase_token)
        print(f"decoded_token: {decoded_token}")
        firebase_uid = decoded_token["uid"]
    else:
        firebase_uid = request.data.get("firebase_uid")

    # Get name and category from request data
    name = request.data.get("name")
    zodiac_sign = request.data.get("zodiac_sign")
    email = request.data.get("email")

    # Find or create the User model based on Firebase UID
    user, _ = User.objects.get_or_create(username=firebase_uid)

    # Update or create Profile for the User
    profile, created = Profile.objects.update_or_create(
        user=user,
        defaults={
            "name": name,
            "zodiac_sign": zodiac_sign,
        },
    )
    if email:
        profile.user.email = email
    profile.user.save()

    level = profile.level
    # Build the absolute URL for the level image
    image_url = request.build_absolute_uri(level.image.url) if level.image else None

    return Response(
        {
            "id": profile.pk,
            "name": profile.name,
            "zodiac_sign": profile.zodiac_sign,
            "level": {
                "name": profile.level.title,
                "description": profile.level.description,
                "image": image_url,
                "questions_count": profile.level.questions_count,
                "questions_answered": profile.level_questions_answered_count,
            },
            "all_answered_questions_count": profile.answered_questions_count,
        }
    )


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" in request.headers:
            # Extract the Firebase token from the "Authorization" header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return None

            # Expect "Authorization: Bearer <token>"
            token = auth_header.split(" ").pop()
            try:
                # Verify the ID token with Firebase
                decoded_token = firebase_auth.verify_id_token(token)
                firebase_uid = decoded_token["uid"]

                # Retrieve or create a User based on the Firebase UID
                user, _ = User.objects.get_or_create(username=firebase_uid)
                return (user, None)
            except Exception as e:
                raise AuthenticationFailed(f"Firebase authentication failed: {str(e)}")
        elif "firebase_uid" in request.data:
            # Retrieve or create a User based on the Firebase UID
            user, _ = User.objects.get_or_create(
                username=request.data.get("firebase_uid")
            )
            return (user, None)
        raise AuthenticationFailed("Firebase authentication failed")


@api_view(["GET", "PATCH"])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def profile_info(request):
    profile = get_object_or_404(Profile, user=request.user)
    level = profile.level
    # Build the absolute URL for the level image
    image_url = request.build_absolute_uri(level.image.url) if level.image else None
    if request.method == "GET":
        return Response(
            {
                "id": profile.pk,
                "name": profile.name,
                "zodiac_sign": profile.zodiac_sign,
                "level": {
                    "name": profile.level.title,
                    "description": profile.level.description,
                    "image": image_url,
                    "questions_count": profile.level.questions_count,
                    "questions_answered": profile.level_questions_answered_count,
                },
                "all_answered_questions_count": profile.answered_questions_count,
            }
        )
    elif request.method == "PATCH":
        # Handle PATCH request to update name and zodiac_sign
        name = request.data.get("name")
        zodiac_sign = request.data.get("zodiac_sign")

        # Update only if fields are provided
        if name is not None:
            profile.name = name
        if zodiac_sign is not None:
            profile.zodiac_sign = zodiac_sign

        profile.save()
        return Response(
            {
                "id": profile.pk,
                "name": profile.name,
                "zodiac_sign": profile.zodiac_sign,
                "level": {
                    "name": profile.level.title,
                    "description": profile.level.description,
                    "image": image_url,
                    "questions_count": profile.level.questions_count,
                    "questions_answered": profile.level_questions_answered_count,
                },
                "all_answered_questions_count": profile.answered_questions_count,
            }
        )


@api_view(["GET"])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    from apps.question.models import Answer

    profile = get_object_or_404(Profile, user=request.user)
    user = profile.user
    Answer.objects.filter(profile=profile)
    profile.delete()
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
