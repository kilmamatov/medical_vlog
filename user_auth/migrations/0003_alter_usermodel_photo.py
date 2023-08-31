# Generated by Django 4.2.4 on 2023-08-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0002_usermodel_is_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermodel",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="static/",
                verbose_name="Фотография",
            ),
        ),
    ]
