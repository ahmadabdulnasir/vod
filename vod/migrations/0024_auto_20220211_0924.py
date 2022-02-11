# Generated by Django 3.2.8 on 2022-02-11 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_cast'),
        ('vod', '0023_review_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='casts',
            field=models.ManyToManyField(blank=True, to='accounts.Cast'),
        ),
        migrations.AddField(
            model_name='series',
            name='casts',
            field=models.ManyToManyField(blank=True, to='accounts.Cast'),
        ),
    ]
