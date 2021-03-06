# Generated by Django 2.2 on 2022-01-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=1500, verbose_name='заголовок')),
                ('content', models.CharField(default='', max_length=1500, verbose_name='содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
                ('flag', models.BooleanField()),
            ],
            options={
                'db_table': 'news',
                'ordering': ['title'],
            },
        ),
    ]
