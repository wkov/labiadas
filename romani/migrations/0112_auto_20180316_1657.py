# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-16 15:57
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0111_auto_20180115_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='adjunt',
            name='productor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjunts', to='romani.Productor'),
        ),
    ]
