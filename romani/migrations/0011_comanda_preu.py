# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0010_auto_20161219_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='preu',
            field=models.FloatField(default=0.0),
        ),
    ]
