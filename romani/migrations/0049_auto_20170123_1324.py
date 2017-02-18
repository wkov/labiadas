# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0048_auto_20170122_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='poblacio',
            field=models.CharField(max_length=40),
        ),
    ]
