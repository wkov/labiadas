# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0016_auto_20161229_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaEntrega',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('dia', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FranjaHoraria',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('inici', models.CharField(max_length=5)),
                ('final', models.CharField(max_length=5)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lloc_entrega',
            field=models.ForeignKey(to='romani.Node', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='diaentrega',
            name='franjes_horaries',
            field=models.ManyToManyField(to='romani.FranjaHoraria'),
        ),
        migrations.AddField(
            model_name='node',
            name='dies_entrega',
            field=models.ManyToManyField(to='romani.DiaEntrega'),
        ),
    ]
