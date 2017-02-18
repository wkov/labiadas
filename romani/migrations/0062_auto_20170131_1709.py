# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0061_auto_20170131_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='punt_lat',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='punt_lng',
            field=models.CharField(max_length=25),
        ),
    ]
