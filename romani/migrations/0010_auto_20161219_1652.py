# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0009_comanda_cancelat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('arxiu', models.FileField(validators=[romani.models.Adjunt.validate_file], upload_to='documents/%Y/%m/%d', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='productor',
            name='adjunt',
        ),
        migrations.AddField(
            model_name='productor',
            name='adjunt',
            field=models.ManyToManyField(to='romani.Adjunt'),
        ),
    ]
