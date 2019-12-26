# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0004_comanda_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=20)),
                ('carrer', models.CharField(max_length=50)),
                ('poblacio', models.CharField(max_length=20)),
                ('codi_postal', models.IntegerField()),
                ('responsable', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='comanda',
            name='lloc_entrega',
            field=models.ForeignKey(to='romani.Node',on_delete=models.CASCADE, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lloc_entrega',
            field=models.ForeignKey(to='romani.Node', on_delete=models.CASCADE, default=1),
            preserve_default=False,
        ),
    ]
