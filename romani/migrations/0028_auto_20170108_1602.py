# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0027_contracte_data_entrega_txt'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='franja_horaria',
            field=models.ForeignKey(to='romani.FranjaHoraria',on_delete=models.CASCADE, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contracte',
            name='franja_horaria',
            field=models.ForeignKey(to='romani.FranjaHoraria', on_delete=models.CASCADE, default=1),
            preserve_default=False,
        ),
    ]
