# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-01-26 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0113_auto_20181009_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaproduccio',
            name='total_uts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producte',
            name='productor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productes', to='romani.Productor'),
        ),
    ]
