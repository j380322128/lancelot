# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from anchor.models import AnchorInfo
from category.models import Category
import enum


# 课程状态
COURSE_LIVE = 1  # 直播
COURSE_RESERVATION = 2  # 预订
COURSE_OVER = 3  # 直播结束
COURSE_REPLAY = 4  # 录播
COURSE_VALIDATE = 5  # 直播待审核状态
COURSE_INVALID = 6  # 直播审核不通过
COURSE_INVALID_7 = 7  # 录播审核不通过
COURSE_INVALID_8 = 8  # 录播待审核状态
COURSE_LIVE_NOUSER = 9  # 正在直播，主播不在

LIVE_STATUS_OVER = 'live_over'
LIVE_STATUS_ON = 'live_on'
LIVE_STATUS_CHOICES = ((LIVE_STATUS_ON, '正在直播'), (LIVE_STATUS_OVER, '直播结束'))

RECORD_STATUS_NO = 'record_no'
RECORD_STATUS_HAVE = 'record_have'


RECORD_STATUS_CHOICES = ((RECORD_STATUS_NO, '不生成录播'), (RECORD_STATUS_HAVE, '生成录播'))

RESOURCE_LOCAL = '3'  # 本地资源
RESOURCE_THIRD = '2'  # 第三方资源
RESOURCE_ULLGET = '1'  # ullget
RESOURCE_STATUS_CHOICES = ((RESOURCE_ULLGET, 'ullget'), (RESOURCE_THIRD, '第三方资源'),
                           (RESOURCE_LOCAL, '本地资源'))

@enum.unique
class RECORD(enum.IntEnum):
    RECORD_ON = 1
    RECORD_OFF = 2

# Create your models here.
class CourseInfo(models.Model):
    """
    课程# 课程直播状态
    """

    course_id = models.CharField(u'课程id', max_length=100, unique=True, null=True)
    title = models.CharField(u'课程标题', max_length=100, help_text=u'不得超过100字符!', null=True)
    description = models.TextField(u'课程简介')

    anchor = models.ForeignKey(AnchorInfo, null=True, related_name="anchor_course")
    support = models.IntegerField(u'点赞', default=0)
    against = models.IntegerField(u'踩', default=0)

    start_time = models.DateTimeField(u'直播开始时间', null=True, auto_now_add=False)
    end_time = models.DateTimeField(u'直播结束时间', null=True)
    create_time = models.DateTimeField(u'创建时间', null=True, auto_now_add=True)

    up_time = models.DateTimeField(u'更新时间', null=True, auto_now=True)
    image = models.ImageField(upload_to='images/course/', null=True)
    status = models.SmallIntegerField(u'直播状态', default=0)
  
    audit = models.IntegerField(default=5, verbose_name=u'审计状态')  
    reason = models.CharField(u"不通过原因", max_length=200, null=True)
    category = models.ForeignKey(Category, null=True)

    sign_num = models.IntegerField(default=0, verbose_name=u'初识报名人数') 
    url = models.CharField(u"地址", max_length=500, null=True)
    active = models.IntegerField("激活", default=1)  # 1-显示  2-隐藏  3-删除
    live_to_record = models.IntegerField(choices=((x.value, x.name.title()) for x in RECORD),
                                         default=RECORD.RECORD_ON.value)

    class Meta:
        db_table = 'course_info'




class Channel(models.Model):
    '''
    视频推流拉流，推流表 基表
    '''
    pulish_url = models.CharField(u"直播rtmp推流", max_length=500, null=True)
    url_rtmp = models.CharField(u"直播rtmp格式拉流地址", max_length=500, null=True)
    url_flv = models.CharField(u"直播flv格式拉流地址", max_length=500, null=True)
    url_hls = models.CharField(u"直播htls拉流地址", max_length=500, null=True)
    appname = models.CharField(u'appname', max_length=100, null=True, help_text='用企业号去表示')
    stream_name = models.CharField(u'stream_name', max_length=100, null=True, help_text='课程号表示')
    status = models.CharField(max_length=20,
                              choices=LIVE_STATUS_CHOICES,
                              default=LIVE_STATUS_ON)
    record_status = models.CharField(max_length=20,
                                     choices=RECORD_STATUS_CHOICES,
                                     default=RECORD_STATUS_NO, help_text='是否生成录播')
    notify_message = models.CharField(max_length=100, null=True, help_text='录播状态描述')
    create_time = models.DateTimeField(u'创建时间', null=True, auto_now_add=True)

    class Meta:
        db_table = "channel_info"


class LiveChannel(models.Model):
    '''
    视频与视频流的中间表
    '''
    # 直播流当前状态, 默认为测试
    STREAM_STATUS_TEST = "test"
    STREAM_STATUS_NORMAL = "normal"
    STREAM_STATUS_CHOICE = (
        (STREAM_STATUS_TEST, "test stream"),
        (STREAM_STATUS_NORMAL, "normal stream")
    )
    video = models.ForeignKey(CourseInfo, 'course_id', null=True, related_name="video_channel")
    channel = models.ForeignKey(Channel, null=True, related_name="live_channel")
    status = models.CharField(max_length=20,
                              choices=LIVE_STATUS_CHOICES,
                              default=LIVE_STATUS_ON)
    notify_message = models.CharField(max_length=100, null=True, help_text='录播状态描述')
    stream_name = models.CharField(max_length=100, null=True, help_text='创建流的三级名')
    create_time = models.DateTimeField(u'创建时间', null=True, auto_now_add=True)
    stream_status = models.CharField(max_length=30, choices=STREAM_STATUS_CHOICE, default=STREAM_STATUS_CHOICE[0][0])

    class Meta:
        db_table = "live_channel"

