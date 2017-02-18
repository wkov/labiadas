# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0003_comanda_cantitat'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='format',
            field=models.ForeignKey(to='romani.TipusProducte', default=1),
            preserve_default=False,
        ),
    ]
