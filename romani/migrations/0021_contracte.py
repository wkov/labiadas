# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('romani', '0020_auto_20170102_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contracte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('cantitat', models.PositiveIntegerField()),
                ('data_comanda', models.DateTimeField(auto_now_add=True)),
                ('data_entrega', models.IntegerField(blank=True, null=True)),
                ('prox_data', models.DateTimeField(blank=True, null=True)),
                ('entregat', models.BooleanField()),
                ('cancelat', models.BooleanField()),
                ('preu', models.FloatField(default=0.0)),
                ('frequencia', models.IntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('format', models.ForeignKey(to='romani.TipusProducte')),
                ('lloc_entrega', models.ForeignKey(to='romani.Node')),
                ('producte', models.ForeignKey(to='romani.Producte')),
            ],
        ),
    ]
