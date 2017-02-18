# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0025_contracte_frequencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracte',
            name='freq_txt',
            field=models.CharField(max_length=30, default=1),
            preserve_default=False,
        ),
    ]
