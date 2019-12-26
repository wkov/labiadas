# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0011_comanda_preu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='producte',
            name='etiqueta',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, to='romani.Etiqueta'),
            preserve_default=False,
        ),
    ]
