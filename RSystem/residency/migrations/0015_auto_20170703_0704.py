# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-03 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0014_auto_20170703_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='User',
        ),
        migrations.AddField(
            model_name='progress',
            name='acc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='residency.Acc'),
            preserve_default=False,
        ),
    ]
