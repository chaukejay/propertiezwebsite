# Generated by Django 5.0.4 on 2024-04-30 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_listingfloorplan_listingimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingimage',
            name='residential_listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='listings.residentiallisting'),
        ),
    ]
