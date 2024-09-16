# Generated by Django 5.0.4 on 2024-06-24 09:44

import agents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_agent_publish_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to=agents.models.agency_image_upload_to)),
            ],
        ),
    ]
