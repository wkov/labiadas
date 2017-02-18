# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('romani', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('data_comanda', models.DateTimeField(auto_now_add=True)),
                ('data_entrega', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('producte', models.ForeignKey(to='romani.Producte')),
            ],
        ),
    ]
