# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0032_auto_20170112_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='a_domicili',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='invitacions',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
