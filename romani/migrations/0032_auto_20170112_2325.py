# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0031_auto_20170111_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='profiles/%Y/%m/%d', null=True, validators=[romani.models.UserProfile.validate_image]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='carrer',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='numero',
            field=models.CharField(blank=True, null=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pis',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='planta',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='poblacio',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
    ]
