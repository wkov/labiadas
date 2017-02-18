# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0035_auto_20170113_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='planta',
        ),
    ]
