from django.db import models


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
