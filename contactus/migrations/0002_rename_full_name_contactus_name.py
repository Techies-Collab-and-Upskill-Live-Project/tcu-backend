# Generated by Django 5.0.2 on 2024-06-20 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contactus", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactus",
            old_name="full_name",
            new_name="name",
        ),
    ]
