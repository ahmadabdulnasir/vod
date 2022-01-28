# Generated by Django 3.2.8 on 2021-12-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0022_auto_20211213_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rate',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='2', help_text='Rating Stars', max_length=1),
            preserve_default=False,
        ),
    ]