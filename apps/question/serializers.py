from rest_framework import serializers

from .models import Question, Level, Answer
from . import models


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    level = LevelSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ["profile"]  # mark profile as read-only


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    answered = serializers.SerializerMethodField()
    skipped = serializers.SerializerMethodField()
    selected_option = serializers.SerializerMethodField()
    level = LevelSerializer()

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "level",
            "option1",
            "option2",
            "option3",
            "option4",
            "answered",
            "skipped",
            "selected_option",
        ]

    def get_answered(self, obj):
        profile = self.context["profile"]
        answer = obj.profile_answer(profile)
        return (
            answer is not None
            and not answer.skipped
            and answer.selected_option is not None
        )

    def get_skipped(self, obj):
        profile = self.context["profile"]
        answer = obj.profile_answer(profile)
        return answer is not None and answer.skipped

    def get_selected_option(self, obj):
        profile = self.context["profile"]
        answer = obj.profile_answer(profile)
        return (
            int(answer.selected_option)
            if (
                answer is not None
                and not answer.skipped
                and answer.selected_option is not None
            )
            else None
        )



class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = [
            'random_id',
            'personal_growth_checked',
            'success_checked',
            'relationships_checked'
        ]