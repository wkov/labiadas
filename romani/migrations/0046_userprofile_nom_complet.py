# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0045_tipusproducte_producte_nom'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nom_complet',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
