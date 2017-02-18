# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0043_auto_20170122_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='producte',
            name='esgotat',
            field=models.BooleanField(default=False),
        ),
    ]
