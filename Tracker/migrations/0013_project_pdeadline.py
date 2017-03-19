# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-30 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0012_project_pcreated'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='pdeadline',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Dead Line'),
            preserve_default=False,
        ),
    ]