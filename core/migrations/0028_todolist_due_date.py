# Generated by Django 4.1.5 on 2023-01-21 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_alter_docs_name_todolist"),
    ]

    operations = [
        migrations.AddField(
            model_name="todolist",
            name="due_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
