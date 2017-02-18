# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0072_auto_20170214_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='producte',
            name='frequencies',
            field=models.ManyToManyField(to='romani.Frequencia', null=True, blank=True),
        ),
    ]
