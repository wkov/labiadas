# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0018_diaentrega_dia_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='dies_entrega',
            field=models.ManyToManyField(related_name='node', to='romani.DiaEntrega'),
        ),
    ]
