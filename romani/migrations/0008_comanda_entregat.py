# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0007_auto_20161219_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='entregat',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
