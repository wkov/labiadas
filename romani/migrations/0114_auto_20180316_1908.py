# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-16 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0113_userprofile_preferits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='positiu',
            field=models.IntegerField(),
        ),
    ]