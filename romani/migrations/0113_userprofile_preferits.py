# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-16 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0112_auto_20180316_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='preferits',
            field=models.ManyToManyField(to='romani.Producte'),
        ),
    ]