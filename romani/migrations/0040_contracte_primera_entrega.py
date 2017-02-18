# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0039_auto_20170116_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracte',
            name='primera_entrega',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
