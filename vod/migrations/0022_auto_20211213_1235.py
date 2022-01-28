# Generated by Django 3.2.8 on 2021-12-13 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('vod', '0021_auto_20211213_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='object_pk',
        ),
        migrations.AlterField(
            model_name='review',
            name='content_type',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'vod'), ('model', 'movie')), models.Q(('app_label', 'vod'), ('model', 'series')), models.Q(('app_label', 'vod'), ('model', 'seriesepisode')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='review',
            name='object_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='PK of Movie, Serie or Series Episode'),
        ),
    ]