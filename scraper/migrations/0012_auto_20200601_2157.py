# Generated by Django 3.0.6 on 2020-06-01 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0011_auto_20200601_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='merk',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='auto',
            name='model',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]