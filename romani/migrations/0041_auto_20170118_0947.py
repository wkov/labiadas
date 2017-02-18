# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0040_contracte_primera_entrega'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productor',
            name='descripcio',
        ),
        migrations.AlterField(
            model_name='productor',
            name='entradilla',
            field=models.TextField(max_length=75),
        ),
    ]
