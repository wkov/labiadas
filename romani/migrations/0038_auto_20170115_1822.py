# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0037_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convidat',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='convidats',
            field=models.ManyToManyField(to='romani.Convidat'),
        ),
    ]
