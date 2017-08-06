# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from anchor.models import AnchorInfo
from category.models import Category
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

    class Meta:
        db_table = 'course_info'

