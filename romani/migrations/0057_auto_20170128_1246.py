# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0056_node_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='text',
            field=models.TextField(max_length=350),
        ),
    ]
