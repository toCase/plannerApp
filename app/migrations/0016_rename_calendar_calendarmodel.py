# Generated by Django 5.0.1 on 2024-02-15 12:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_calendar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Calendar',
            new_name='CalendarModel',
        ),
    ]
