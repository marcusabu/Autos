# Generated by Django 3.0.6 on 2020-05-31 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_auto_bron'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auto',
            old_name='isBenzine',
            new_name='is_benzine',
        ),
        migrations.RenameField(
            model_name='auto',
            old_name='isHandgeschakeld',
            new_name='is_handgeschakeld',
        ),
    ]
