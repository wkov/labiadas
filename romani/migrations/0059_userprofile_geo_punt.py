# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0058_auto_20170128_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='geo_punt',
            field=geoposition.fields.GeopositionField(max_length=42, default=1),
            preserve_default=False,
        ),
    ]
