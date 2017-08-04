# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


@register.filter(name='in_groups')
def in_groups(user, group_name_str):
    '''
    检测用户是否在指定的组中
    :param user:
    :param group_name_str:
    :return:
    '''
    group_name_list = str(group_name_str).split(',')
    groups = Group.objects.filter(name__in=group_name_list)
    return user.groups.all().first() in groups

