# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-13 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_channel_livechannel'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='live_to_record',
            field=models.IntegerField(choices=[(1, b'Record_On'), (2, b'Record_Off')], default=1),
        ),
    ]
