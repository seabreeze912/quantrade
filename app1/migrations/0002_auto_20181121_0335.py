# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-20 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btcdailydata',
            name='dateTime',
            field=models.DateTimeField(unique=True),
        ),
    ]