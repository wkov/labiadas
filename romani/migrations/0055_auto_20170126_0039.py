# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0054_auto_20170126_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etiqueta',
            name='img',
            field=models.FileField(default=1, upload_to='etiquetes'),
            preserve_default=False,
        ),
    ]
