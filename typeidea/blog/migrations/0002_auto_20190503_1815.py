# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-03 10:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='creted_time',
            new_name='created_time',
        ),
    ]