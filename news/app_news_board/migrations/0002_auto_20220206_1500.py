# Generated by Django 2.2 on 2022-02-06 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_news_board', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={},
        ),
        migrations.RenameField(
            model_name='news',
            old_name='flag',
            new_name='is_active',
        ),
        migrations.AlterModelTable(
            name='news',
            table=None,
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='anonymous', max_length=50)),
                ('text', models.CharField(default='', max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_news', to='app_news_board.News', verbose_name='новость')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор комментария')),
            ],
        ),
    ]
