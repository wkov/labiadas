# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0023_auto_20170107_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracte',
            name='frequencia',
        ),
    ]
