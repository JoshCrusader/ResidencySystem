# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-03 06:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0012_auto_20170703_0506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progress',
            old_name='acc',
            new_name='User',
        ),
    ]