# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0010_sprint_screated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tsprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracker.sprint'),
        ),
    ]
