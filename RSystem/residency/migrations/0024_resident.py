# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-07 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0023_auto_20170706_0133'),
    ]

    operations = [
        migrations.CreateModel(
            name='resident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdate', models.DateTimeField(editable=False)),
                ('edate', models.DateTimeField(editable=False, null=True)),
                ('acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residency.Acc')),
            ],
        ),
    ]