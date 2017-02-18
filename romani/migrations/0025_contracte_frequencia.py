# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0024_remove_contracte_frequencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracte',
            name='frequencia',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
