# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0033_auto_20170113_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='pis',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
