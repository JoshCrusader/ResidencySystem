# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0007_auto_20170627_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='stat',
            field=models.CharField(default='active', max_length=100),
            preserve_default=False,
        ),
    ]
