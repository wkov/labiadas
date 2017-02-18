# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0028_auto_20170108_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='numero',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
