# Generated by Django 2.2 on 2022-02-15 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0009_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, default='profile_images/defaultuser.png', null=True, upload_to='profile_images/'),
        ),
    ]
