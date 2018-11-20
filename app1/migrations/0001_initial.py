# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-20 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BtcDailyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('close', models.FloatField(max_length=30)),
                ('dateTime', models.DateTimeField()),
                ('high', models.FloatField(max_length=30)),
                ('low', models.FloatField(max_length=30)),
                ('open', models.FloatField(max_length=30)),
                ('symbol', models.CharField(max_length=20)),
                ('vol', models.FloatField(max_length=30)),
            ],
        ),
    ]
