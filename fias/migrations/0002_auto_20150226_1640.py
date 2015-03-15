# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addrobj',
            name='actstatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addrobj',
            name='livestatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='house',
            name='eststatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
