# Generated by Django 4.1.5 on 2023-01-15 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_alter_budget_remaining_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="amount_remaining",
            field=models.IntegerField(default=0),
        ),
    ]
