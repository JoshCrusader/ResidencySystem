# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-06 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0021_project_cubes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='cubes',
        ),
        migrations.AddField(
            model_name='team',
            name='cubes',
            field=models.CharField(default='LEXELL', max_length=20),
            preserve_default=False,
        ),
    ]