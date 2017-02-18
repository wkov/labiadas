# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0022_auto_20170107_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comanda',
            name='data_fi',
        ),
        migrations.AddField(
            model_name='contracte',
            name='data_fi',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
