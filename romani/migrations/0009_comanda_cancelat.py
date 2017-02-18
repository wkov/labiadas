# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0008_comanda_entregat'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='cancelat',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
