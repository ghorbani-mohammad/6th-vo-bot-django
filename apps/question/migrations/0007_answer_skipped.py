# Generated by Django 4.2.9 on 2024-11-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_promptsetting_max_tokens_promptsetting_temperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='skipped',
            field=models.BooleanField(default=False),
        ),
    ]
