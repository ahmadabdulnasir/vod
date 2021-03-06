# Generated by Django 3.2.8 on 2021-10-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0002_auto_20211006_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, to='vod.Genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='posters',
            field=models.ManyToManyField(blank=True, to='vod.Poster'),
        ),
    ]
