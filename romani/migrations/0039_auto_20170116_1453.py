# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0038_auto_20170115_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracte',
            name='prox_data',
        ),
        migrations.AddField(
            model_name='contracte',
            name='prox_no',
            field=models.NullBooleanField(),
        ),
    ]
