# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avaron', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='seed',
            field=models.BigIntegerField(default=0),
        ),
    ]