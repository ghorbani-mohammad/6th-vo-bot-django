# Generated by Django 4.2.9 on 2024-11-13 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_answer_skipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='selected_option',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
