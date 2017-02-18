# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0012_auto_20161221_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='productor',
            name='mail',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
