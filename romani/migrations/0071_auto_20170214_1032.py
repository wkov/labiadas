# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0070_auto_20170213_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='node',
            name='freq_txt',
        ),
        migrations.RemoveField(
            model_name='node',
            name='frequencia',
        ),
        migrations.AddField(
            model_name='node',
            name='frequencia',
            field=models.ManyToManyField(blank=True, null=True, to='romani.Frequencia'),
        ),
    ]
