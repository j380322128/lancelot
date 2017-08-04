# -*- coding: utf-8 -*-

import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


REDIRECT_FIELD_NAME = 'next'


def generate_username():
    '''
    生成username
    :return:
    '''
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    my_slice = random.sample(code_list, 8)  # 从list中随机获取8个元素，作为一个片断返回
    username = ''.join(my_slice)
    return 'UG' + username


def get_unique_username():
    '''
    生成唯一的用户名
    :return:
    '''
    # 生成未使用，且唯一的username
    user_list = True
    username = None
    while user_list:
        username = generate_username()
        user_list = User.objects.filter(username=username)
    return username


def user_info_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    if not login_url:
        login_url = 'user:login'
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


