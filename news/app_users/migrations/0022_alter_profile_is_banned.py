# Generated by Django 3.2.6 on 2022-04-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0021_rename_is_verified_profile_is_banned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_banned',
            field=models.BooleanField(default=False, null=True, verbose_name='banned'),
        ),
    ]
