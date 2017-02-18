# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0041_auto_20170118_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='producte',
            name='nodes',
            field=models.ManyToManyField(blank=True, to='romani.Node', null=True),
        ),
    ]
