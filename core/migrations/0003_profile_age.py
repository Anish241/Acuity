# Generated by Django 4.1.5 on 2023-01-14 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_profile_profileimg"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile", name="age", field=models.IntegerField(default=0),
        ),
    ]
