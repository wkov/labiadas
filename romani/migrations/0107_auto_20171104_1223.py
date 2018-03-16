# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-04 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0106_auto_20171028_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='producte',
            name='foto',
            field=models.FileField(null=True, upload_to='productes/%Y/%m/%d', validators=[romani.models.Producte.validate_file]),
        ),
    ]