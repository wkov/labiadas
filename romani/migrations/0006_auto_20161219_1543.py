# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0005_auto_20161219_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='data_entrega',
            field=models.DateTimeField(blank=True),
        ),
    ]
