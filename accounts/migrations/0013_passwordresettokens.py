# Generated by Django 3.2.8 on 2022-02-01 13:46

import core.utils.units
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0012_alter_subscriptionplan_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(default=core.utils.units.genserial, max_length=10, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('sent_count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Passwords Reset Tokens',
                'ordering': ('-updated',),
            },
        ),
    ]
