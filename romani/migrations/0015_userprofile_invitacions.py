# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0014_productor_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='invitacions',
            field=models.IntegerField(default=20),
        ),
    ]
