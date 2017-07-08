# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-03 07:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('residency', '0015_auto_20170703_0704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='acc',
        ),
        migrations.AddField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]