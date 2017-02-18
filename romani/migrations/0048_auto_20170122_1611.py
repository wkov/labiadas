# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0047_auto_20170122_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(validators=[romani.models.UserProfile.validate_image], upload_to='profiles/%Y/%m/%d', default=1),
            preserve_default=False,
        ),
    ]
