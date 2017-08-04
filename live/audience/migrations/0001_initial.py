# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-01 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'', max_length=30, verbose_name='\u59d3\u540d')),
                ('sex', models.IntegerField(choices=[(1, '\u7537'), (0, '\u5973')], default=1)),
                ('age', models.IntegerField(blank=True, default=30, null=True)),
                ('tel', models.CharField(default=b'', max_length=50, null=True)),
                ('passwd', models.CharField(default=b'', max_length=100, null=True)),
                ('e_mail', models.CharField(default=b'', max_length=50, null=True)),
                ('title', models.TextField(default=b'', null=True, verbose_name='\u5934\u8854')),
                ('image', models.ImageField(null=True, upload_to=b'images/user_info/')),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]