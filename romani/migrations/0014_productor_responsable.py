# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('romani', '0013_productor_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='productor',
            name='responsable',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
