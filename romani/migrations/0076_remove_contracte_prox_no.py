# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 23:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0075_auto_20170311_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracte',
            name='prox_no',
        ),
    ]
