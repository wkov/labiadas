# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0021_contracte'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='data_fi',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diaentrega',
            name='dia_num',
            field=models.IntegerField(),
        ),
    ]
