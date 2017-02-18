# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0042_producte_nodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipusproducte',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(blank=True, upload_to='profiles/%Y/%m/%d', validators=[romani.models.UserProfile.validate_image], null=True),
        ),
    ]
