# Generated by Django 3.2.8 on 2022-02-11 08:24

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_passwordresettokens'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fullname', models.CharField(max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.cast_image_location)),
                ('bio', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cast_profile', to='accounts.userprofile')),
            ],
            options={
                'verbose_name': 'Cast Profile',
                'verbose_name_plural': 'Casts Profiles',
                'ordering': ['-updated', 'fullname'],
            },
        ),
    ]
