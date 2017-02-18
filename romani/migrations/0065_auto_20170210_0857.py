# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0064_producte_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etiqueta',
            name='nom',
            field=models.CharField(max_length=15),
        ),
    ]
