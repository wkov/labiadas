# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0030_auto_20170110_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producte',
            name='entradilla',
            field=models.TextField(max_length=75),
        ),
    ]
