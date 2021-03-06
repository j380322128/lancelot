# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-10 02:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_courseinfo_sign_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pulish_url', models.CharField(max_length=500, null=True, verbose_name='\u76f4\u64adrtmp\u63a8\u6d41')),
                ('url_rtmp', models.CharField(max_length=500, null=True, verbose_name='\u76f4\u64adrtmp\u683c\u5f0f\u62c9\u6d41\u5730\u5740')),
                ('url_flv', models.CharField(max_length=500, null=True, verbose_name='\u76f4\u64adflv\u683c\u5f0f\u62c9\u6d41\u5730\u5740')),
                ('url_hls', models.CharField(max_length=500, null=True, verbose_name='\u76f4\u64adhtls\u62c9\u6d41\u5730\u5740')),
                ('appname', models.CharField(help_text='\u7528\u4f01\u4e1a\u53f7\u53bb\u8868\u793a', max_length=100, null=True, verbose_name='appname')),
                ('stream_name', models.CharField(help_text='\u8bfe\u7a0b\u53f7\u8868\u793a', max_length=100, null=True, verbose_name='stream_name')),
                ('status', models.CharField(choices=[('live_on', '\u6b63\u5728\u76f4\u64ad'), ('live_over', '\u76f4\u64ad\u7ed3\u675f')], default='live_on', max_length=20)),
                ('record_status', models.CharField(choices=[('record_no', '\u4e0d\u751f\u6210\u5f55\u64ad'), ('record_have', '\u751f\u6210\u5f55\u64ad')], default='record_no', help_text='\u662f\u5426\u751f\u6210\u5f55\u64ad', max_length=20)),
                ('notify_message', models.CharField(help_text='\u5f55\u64ad\u72b6\u6001\u63cf\u8ff0', max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'db_table': 'channel_info',
            },
        ),
        migrations.CreateModel(
            name='LiveChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('live_on', '\u6b63\u5728\u76f4\u64ad'), ('live_over', '\u76f4\u64ad\u7ed3\u675f')], default='live_on', max_length=20)),
                ('notify_message', models.CharField(help_text='\u5f55\u64ad\u72b6\u6001\u63cf\u8ff0', max_length=100, null=True)),
                ('stream_name', models.CharField(help_text='\u521b\u5efa\u6d41\u7684\u4e09\u7ea7\u540d', max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('stream_status', models.CharField(choices=[('test', 'test stream'), ('normal', 'normal stream')], default='test', max_length=30)),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='live_channel', to='course.Channel')),
                ('video', models.ForeignKey(null=True, on_delete='id', related_name='video_channel', to='course.CourseInfo', to_field='course_id')),
            ],
            options={
                'db_table': 'live_channel',
            },
        ),
    ]
