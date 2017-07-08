# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-03 05:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residency', '0011_auto_20170628_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=2000)),
                ('cdate', models.DateTimeField(editable=False)),
                ('acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residency.Acc')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residency.Project')),
            ],
        ),
        migrations.AlterField(
            model_name='status',
            name='value',
            field=models.CharField(max_length=45),
        ),
    ]
