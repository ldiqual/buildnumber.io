# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-17 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160117_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountemail',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('package', 'build_number')]),
        ),
    ]
