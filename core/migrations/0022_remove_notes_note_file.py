# Generated by Django 4.1.5 on 2023-01-16 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_file"),
    ]

    operations = [
        migrations.RemoveField(model_name="notes", name="note_file",),
    ]
