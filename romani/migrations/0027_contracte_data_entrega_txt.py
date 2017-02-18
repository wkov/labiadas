# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0026_contracte_freq_txt'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracte',
            name='data_entrega_txt',
            field=models.CharField(max_length=10, default=1),
            preserve_default=False,
        ),
    ]
