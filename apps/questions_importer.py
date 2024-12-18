import csv
import sys
import os

import django


def initial():
    sys.path.append("..")
    os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"
    django.setup()


initial()

from apps.question.models import Level, Question  # Adjust the import path if necessary

file_path = "Questions3.csv"  # Update with your file path if necessary

with open(file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    current_level = None
    for row in reader:
        # Check if there's a level in the current row
        if row["Levels"]:
            # Extract level title from row and clean it up
            level_title = row["Levels"].split(" (")[1].rstrip(")")
            level, created = Level.objects.get_or_create(title=level_title)
            current_level = level  # Set current level

        # Create Question associated with the current level
        question_text = row["Question"]
        option1 = row["A"]
        option2 = row["B"]
        option3 = row.get("C", "")
        option4 = row.get("D", "")

        Question.objects.create(
            question_text=question_text,
            level=current_level,
            option1=option1,
            option2=option2,
            option3=option3 if option3 else None,
            option4=option4 if option4 else None,
        )
