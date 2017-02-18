# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0029_node_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='carrer',
            field=models.CharField(max_length=30, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='numero',
            field=models.CharField(max_length=5, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pis',
            field=models.CharField(max_length=10, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='planta',
            field=models.CharField(max_length=10, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='poblacio',
            field=models.CharField(max_length=30, default=1),
            preserve_default=False,
        ),
    ]
