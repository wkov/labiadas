# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-17 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0116_userprofile_direccio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='frequencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='romani.Frequencia'),
        ),
    ]
