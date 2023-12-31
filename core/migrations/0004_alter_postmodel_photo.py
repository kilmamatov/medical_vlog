# Generated by Django 4.2.4 on 2023-08-31 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_postmodel_slug_commentmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postmodel",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="static/",
                verbose_name="Фотография",
            ),
        ),
    ]
