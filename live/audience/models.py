# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):

    owner = models.OneToOneField(User, related_name='owner', null=True)
    user_id = models.CharField(max_length=100, unique=True, null=True)

    name = models.CharField(max_length=30, verbose_name=u'姓名', default='')
    
    sex = models.IntegerField(default=1, choices=((1, u'男'), (0, u'女')))
    age = models.IntegerField(null=True, default=30, blank=True)
    tel = models.CharField(max_length=50, null=True, unique=True)
    passwd = models.CharField(max_length=100, default='', null=True)
    e_mail = models.CharField(max_length=50, null=True, default='')
    title = models.TextField(verbose_name=u'头衔', null=True, default='')
    image = models.ImageField(upload_to='images/user_info/', null=True)
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
        db_table = 'user_info'