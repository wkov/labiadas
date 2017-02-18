# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0019_auto_20170102_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='position',
            field=geoposition.fields.GeopositionField(default=1, max_length=42),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comanda',
            name='cantitat',
            field=models.PositiveIntegerField(),
        ),
    ]
