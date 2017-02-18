# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0065_auto_20170210_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='freq_txt',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='node',
            name='frequencia',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
