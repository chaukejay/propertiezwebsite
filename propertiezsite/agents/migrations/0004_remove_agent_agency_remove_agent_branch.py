# Generated by Django 5.0.4 on 2024-06-24 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_agency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='branch',
        ),
    ]
