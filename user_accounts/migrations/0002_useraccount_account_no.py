# Generated by Django 5.0.2 on 2024-03-09 00:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="account_no",
            field=models.IntegerField(default=100000, unique=True),
        ),
    ]
