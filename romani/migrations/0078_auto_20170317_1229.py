# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0077_auto_20170316_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='codi_postal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='numero',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='pis',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
