# Generated by Django 3.2.8 on 2021-10-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0005_auto_20211015_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movieposter',
            options={'ordering': ['-updated'], 'verbose_name': 'Movie Poster', 'verbose_name_plural': 'Movies Posters'},
        ),
        migrations.AlterField(
            model_name='movieposter',
            name='image',
            field=models.ImageField(upload_to='posters'),
        ),
    ]
