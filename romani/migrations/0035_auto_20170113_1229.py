# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0034_node_pis'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='lloc_entrega',
            new_name='lloc_entrega_perfil',
        ),
    ]
