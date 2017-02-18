# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0071_auto_20170214_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='frequencia',
        ),
        migrations.AddField(
            model_name='node',
            name='frequencies',
            field=models.ManyToManyField(to='romani.Frequencia', blank=True, null=True),
        ),
    ]
