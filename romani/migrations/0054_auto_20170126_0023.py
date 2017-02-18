# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0053_etiqueta_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etiqueta',
            name='img',
            field=models.ImageField(null=True, upload_to='etiquetes'),
        ),
    ]
