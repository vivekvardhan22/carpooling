# Generated by Django 5.1.4 on 2025-01-06 18:58

import authy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=authy.models.user_directory_path, verbose_name='Picture'),
        ),
    ]
