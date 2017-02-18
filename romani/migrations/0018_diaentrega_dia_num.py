# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0017_auto_20161230_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaentrega',
            name='dia_num',
            field=models.IntegerField(max_length=2, default=1),
            preserve_default=False,
        ),
    ]
