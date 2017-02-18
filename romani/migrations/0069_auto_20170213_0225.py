# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0068_remove_tipusproducte_producte_nom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productor',
            name='datahora',
        ),
        migrations.AddField(
            model_name='diaentrega',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 13, 2, 25, 33, 268687, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producte',
            name='dies_entrega',
            field=models.ManyToManyField(null=True, blank=True, to='romani.DiaEntrega'),
        ),
        migrations.AlterField(
            model_name='producte',
            name='formats',
            field=models.ManyToManyField(related_name='producte', to='romani.TipusProducte'),
        ),
    ]
