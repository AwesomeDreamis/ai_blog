# Generated by Django 2.2 on 2022-02-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0007_auto_20220212_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='news_count',
            field=models.IntegerField(default=0, verbose_name='количество постов'),
        ),
    ]
