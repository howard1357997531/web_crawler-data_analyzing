# Generated by Django 4.1 on 2022-08-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_student_chinese_student_code_student_english_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student", name="code", field=models.CharField(max_length=150),
        ),
    ]
