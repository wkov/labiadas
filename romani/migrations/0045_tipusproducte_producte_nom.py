# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0044_producte_esgotat'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipusproducte',
            name='producte_nom',
            field=models.CharField(max_length=20, default=1),
            preserve_default=False,
        ),
    ]
