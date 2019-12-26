# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0051_auto_20170125_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='nou_usuari',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='key_nou_usuari', blank=True, null=True),
        ),
    ]
