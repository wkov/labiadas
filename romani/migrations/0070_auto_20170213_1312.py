# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0069_auto_20170213_0225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diaentrega',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='diaentrega',
            name='dia_num',
        ),
    ]
