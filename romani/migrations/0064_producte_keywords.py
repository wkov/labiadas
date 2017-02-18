# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0063_auto_20170131_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='producte',
            name='keywords',
            field=models.TextField(blank=True),
        ),
    ]
