# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-11 11:05
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0100_auto_20170603_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comanda',
            name='cancelat',
        ),
        migrations.RemoveField(
            model_name='comanda',
            name='entregat',
        ),
        migrations.RemoveField(
            model_name='comanda',
            name='lloc_entrega',
        ),
        migrations.RemoveField(
            model_name='comanda',
            name='producte',
        ),
        migrations.RemoveField(
            model_name='diaproduccio',
            name='dies_entrega',
        ),
        migrations.AddField(
            model_name='comanda',
            name='externa',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='diaproduccio',
            name='caducitat',
            field=models.DateField(default=datetime.datetime(2017, 6, 11, 11, 5, 26, 152486)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='stock_ini',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
