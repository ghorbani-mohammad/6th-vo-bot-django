from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ("admin", "Admin"),
    ("user", "User"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    name = models.CharField(max_length=255, null=True, blank=True)
    zodiac_sign = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def personal_growth_horoscopy(self):
        return "You are growing"

    @property
    def success_horoscopy(self):
        return "You are successful"

    @property
    def relationship_horoscopy(self):
        return "You have a good relationship"
