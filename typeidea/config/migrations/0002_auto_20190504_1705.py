# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-04 09:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sidebar',
            options={'verbose_name': '侧边栏', 'verbose_name_plural': '侧边栏'},
        ),
    ]
