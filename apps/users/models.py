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
    def level_questions_answered_count(self):
        from apps.question.models import Answer

        level = self.level
        return Answer.objects.filter(profile=self, question__level=level).count()

    @property
    def answered_questions_count(self):
        return self.answered_questions.count()

    @property
    def answered_questions(self):
        from apps.question.models import Question

        return Question.objects.filter(answer__profile=self).distinct()

    @property
    def personal_growth_horoscopy(self):
        return "You are growing"

    @property
    def success_horoscopy(self):
        return "You are successful"

    @property
    def relationship_horoscopy(self):
        return "You have a good relationship"

    @property
    def level(self):
        print("In the profile level property")
        from apps.question.models import Level, Answer

        levels = Level.objects.order_by("pk")
        for level in levels:
            print(f"level: {level}")
            questions_count = level.questions_count
            answered_questions_count = Answer.objects.filter(
                profile=self, question__level=level
            ).count()

            if answered_questions_count < questions_count:
                return level  # or return level object if needed
        # If all levels are fully answered
        return levels.last() if levels.exists() else None
