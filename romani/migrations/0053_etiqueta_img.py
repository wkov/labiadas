# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0052_auto_20170125_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='etiqueta',
            name='img',
            field=models.ImageField(null=True, upload_to='documents/%Y/%m/%d'),
        ),
    ]
