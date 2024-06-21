# Generated by Django 5.0.1 on 2024-02-20 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_msheduletemplate_delete_shedulemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='msheduletemplate',
            name='firm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.firm'),
            preserve_default=False,
        ),
    ]