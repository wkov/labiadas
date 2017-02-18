# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0015_userprofile_invitacions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='invitacions',
            field=models.IntegerField(null=True, default=20, blank=True),
        ),
    ]
