# Generated by Django 2.2 on 2022-03-25 19:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0016_auto_20220325_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(default=None, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='subscribers'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(default=None, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscriptions'),
        ),
    ]