# Generated by Django 5.0.4 on 2024-05-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_alter_listingenquiry_add_to_leads_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingenquiry',
            name='subscribe_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listingenquiry',
            name='unsubscribe_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
