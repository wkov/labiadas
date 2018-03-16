# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 19:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('romani', '0098_auto_20170530_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positiu', models.BooleanField()),
                ('comanda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='romani.Comanda')),
                ('contracte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='romani.Contracte')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]