# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-20 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0014_auto_20170320_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='status',
            field=models.CharField(choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')], default='Green', max_length=10),
        ),
    ]
