# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0067_auto_20170211_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipusproducte',
            name='producte_nom',
        ),
    ]
