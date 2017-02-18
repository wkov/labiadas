# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('romani', '0050_remove_userprofile_nom_complet'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='nou_usuari',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, related_name='key_nou_usuari'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='key',
            name='usuari',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
