# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0057_auto_20170128_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='text',
            field=models.TextField(max_length=1000),
        ),
    ]
