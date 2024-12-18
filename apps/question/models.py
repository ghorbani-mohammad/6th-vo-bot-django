from django.db import models

from apps.users.models import Profile


class Level(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="levels/", null=True, blank=True)

    def __str__(self):
        return f"({self.pk} - {self.title})"

    @property
    def questions_count(self):
        return self.question_set.count()


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    option1 = models.CharField(max_length=500, null=True, blank=True)
    option2 = models.CharField(max_length=500, null=True, blank=True)
    option3 = models.CharField(max_length=500, null=True, blank=True)
    option4 = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"({self.pk} - {self.question_text})"

    def profile_answer(self, profile):
        return Answer.objects.filter(question=self, profile=profile).last()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=500, null=True, blank=True)
    skipped = models.BooleanField(default=False)
    selected_option_text = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"({self.pk} - {self.question} - {self.profile})"


class PromptSetting(models.Model):
    personal_growth = models.CharField(max_length=500)
    personal_growth_todo = models.CharField(max_length=500, blank=True, null=True)
    success = models.CharField(max_length=500)
    success_todo = models.CharField(max_length=500, blank=True, null=True)
    relationships = models.CharField(max_length=500)
    relationships_todo = models.CharField(max_length=500, blank=True, null=True)
    affirmation = models.CharField(max_length=500, null=True, blank=True)
    thinker = models.CharField(max_length=500, null=True, blank=True)
    quote = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    temperature = models.FloatField(default=0)
    max_tokens = models.IntegerField(default=200)
    cache_duration = models.IntegerField(default=24 * 60 * 60, help_text="In seconds")

    def __str__(self):
        return f"({self.pk})"


class HoroscopeLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    horoscope = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.pk} - {self.profile})"


class Todo(models.Model):
    random_id = models.CharField(max_length=100, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    todos = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    personal_growth_checked = models.BooleanField(default=False)
    success_checked = models.BooleanField(default=False)
    relationships_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.pk} - {self.profile})"
