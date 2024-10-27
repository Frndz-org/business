# Generated by Django 5.0.6 on 2024-10-27 07:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0002_alter_industry_options_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='industry',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
