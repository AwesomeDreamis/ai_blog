# Generated by Django 3.2.6 on 2022-05-01 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0022_alter_profile_is_banned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]
