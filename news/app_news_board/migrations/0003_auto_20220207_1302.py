# Generated by Django 2.2 on 2022-02-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news_board', '0002_auto_20220206_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default='anonymous', max_length=50, null=True),
        ),
    ]