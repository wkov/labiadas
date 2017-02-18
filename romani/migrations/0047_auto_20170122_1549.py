# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0046_userprofile_nom_complet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='profiles/%Y/%m/%d', validators=[romani.models.UserProfile.validate_image], null=True),
        ),
    ]
