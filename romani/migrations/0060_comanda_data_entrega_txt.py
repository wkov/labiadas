# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0059_userprofile_geo_punt'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='data_entrega_txt',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
