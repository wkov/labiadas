# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0049_auto_20170123_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='nom_complet',
        ),
    ]
