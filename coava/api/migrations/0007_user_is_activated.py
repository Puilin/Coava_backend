# Generated by Django 4.1.7 on 2023-03-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_user_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
    ]
