# Generated by Django 3.2.8 on 2021-11-08 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0019_auto_20211108_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='genre',
            new_name='genres',
        ),
    ]
