# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AnchorInfo(models.Model):
    user_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=30, verbose_name=u'姓名', default='')
    native = models.CharField(max_length=100, verbose_name=u'出生地', null=True, default='')
    sex = models.IntegerField(default=1, choices=((1, u'男'), (0, u'女')))
    age = models.IntegerField(null=True, default=30)
    tel = models.CharField(max_length=50, null=True, unique=False, default='')
    e_mail = models.CharField(max_length=50, null=True, default='')
    title = models.TextField(verbose_name=u'头衔', null=True, default='')
    image = models.ImageField(upload_to='images/anchor/', null=True)
    description = models.TextField(verbose_name=u'个性签名', null=True)
    character_name = models.CharField(max_length=100, unique=True, null=True, verbose_name="个性域名")
    audit = models.IntegerField(default=5, verbose_name=u'审计状态')  # 0-审核不通过 1-待审核　2-通过待上架　3-已上架
    reason = models.CharField(max_length=300, verbose_name=u'审批备注', null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def get_sex(self):
        gender = u"女"
        if self.sex == 1:
            gender = u"男"
        return gender

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'anchor_info'

