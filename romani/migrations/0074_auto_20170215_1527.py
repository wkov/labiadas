# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0073_producte_frequencies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='profiles/%Y/%m/%d', blank=True, null=True, validators=[romani.models.UserProfile.validate_image]),
        ),
    ]
