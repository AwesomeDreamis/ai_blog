# Generated by Django 3.2.6 on 2022-04-05 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0020_alter_profile_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_verified',
            new_name='is_banned',
        ),
    ]
