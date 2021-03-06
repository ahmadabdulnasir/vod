# Generated by Django 3.2.8 on 2021-10-23 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_marchant_created_by'),
        ('vod', '0008_auto_20211015_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='uploaded_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='uploaded_movies', to='accounts.userprofile'),
            preserve_default=False,
        ),
    ]
