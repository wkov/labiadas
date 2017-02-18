# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0066_auto_20170211_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diaentrega',
            name='franjes_horaries',
            field=models.ManyToManyField(to='romani.FranjaHoraria', related_name='dia'),
        ),
    ]
