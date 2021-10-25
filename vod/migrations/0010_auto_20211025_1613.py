# Generated by Django 3.2.8 on 2021-10-25 15:13

from django.db import migrations, models
import vod.models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0009_movie_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='access_level',
            field=models.CharField(choices=[('free', 'Free'), ('premium', 'Premium'), ('exclusive', 'Exclusive')], default='free', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=vod.models.movie_locations),
        ),
    ]
