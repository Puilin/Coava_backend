# Generated by Django 4.1.7 on 2023-03-31 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_daily_delete_meme"),
    ]

    operations = [
        migrations.CreateModel(
            name="Buzz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("detail", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Meme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("detail", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
            ],
        ),
    ]