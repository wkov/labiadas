# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0060_comanda_data_entrega_txt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='geo_punt',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='punt_lat',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='punt_lng',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
