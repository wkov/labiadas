# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-15 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0110_producte_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producte',
            name='thumb',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
