# Generated by Django 4.1.5 on 2023-01-15 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_expense_amount_remaining"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="amount_remaining",
            field=models.IntegerField(default=-1),
        ),
    ]
