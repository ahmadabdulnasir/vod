# Generated by Django 3.2.8 on 2021-10-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('free_user', 'Free User'), ('premium_user', 'Premium User'), ('marchant', 'Marchant'), ('staff', 'Staff'), ('admin', 'Admin'), ('super_admin', 'Super Admin')], default='free_user', max_length=50),
        ),
    ]
