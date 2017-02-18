# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0055_auto_20170126_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='text',
            field=models.CharField(default=1, max_length=350),
            preserve_default=False,
        ),
    ]
