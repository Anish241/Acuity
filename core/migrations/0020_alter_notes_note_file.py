# Generated by Django 4.1.5 on 2023-01-16 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_rename_note_name_notes_title_notes_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notes",
            name="note_file",
            field=models.FileField(default="blank.pdf", upload_to="notes"),
        ),
    ]
