# Generated by Django 5.0.4 on 2024-06-24 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_agent_agency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='integrations',
        ),
    ]
