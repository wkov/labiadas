# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import romani.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producte',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=20)),
                ('descripcio', models.TextField(blank=True, default='')),
                ('datahora', models.DateTimeField(auto_now_add=True)),
                ('adjunt', models.FileField(null=True, upload_to='documents/%Y/%m/%d', validators=[romani.models.Producte.validate_file])),
                ('entradilla', models.TextField()),
                ('cuerpo', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Productor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=20)),
                ('descripcio', models.TextField(blank=True, default='')),
                ('datahora', models.DateTimeField(auto_now_add=True)),
                ('adjunt', models.FileField(null=True, upload_to='documents/%Y/%m/%d')),
                ('entradilla', models.TextField()),
                ('cuerpo', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipusProducte',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=20)),
                ('preu', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('bio', models.TextField(null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='producte',
            name='formats',
            field=models.ManyToManyField(to='romani.TipusProducte'),
        ),
        migrations.AddField(
            model_name='producte',
            name='productor',
            field=models.ForeignKey(to='romani.Productor', on_delete=models.CASCADE),
        ),
    ]
