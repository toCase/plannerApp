# Generated by Django 5.0.1 on 2024-03-13 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_mnotes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specmodel',
            options={'ordering': ['spec_active', 'spec_fname']},
        ),
        migrations.AlterField(
            model_name='specmodel',
            name='spec_lname',
            field=models.CharField(max_length=30),
        ),
    ]