# -*- coding: utf-8 -*-
import requests
import datetime
import hashlib
import uuid
import urllib
import json
import operator
from functools import reduce
import logging

from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import ListView, CreateView, FormView, TemplateView, DetailView, View
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction

from models import UserInfo
from utils import get_unique_username
from sdk.xxx import VerificationCode


# 1 注册 2 手机登录 3 第三方绑定 4 修改密码 5 修改手机号码
CODE_REGISTRATION = '1'
CODE_LOGIN = '2'
CODE_BIND = '3'
CODE_RESET_PASSWORD = '4'
CODE_RESET_PHONE = '5'

# @method_decorator(login_required, name='dispatch')
# # @method_decorator(user_group_required('admin,staff'), name='dispatch')
# class Index(ListView):
#     '''
#     前端用户首页
#     '''
#     template_name = 'user/user_table.html'
#     # paginate_by = PAGE_NUM
#     context_object_name = 'obj_list'

#     def get_context_data(self, **kwargs):
#         context = super(Index, self).get_context_data(**kwargs)
#         context['PRIMARY_ACCOUNT_TYPE'] = settings.PRIMARY_ACCOUNT_TYPE # accountType__name
#         return context

#     def get_queryset(self):
#         during_dict = {'day': u'一天', 'week': u'一周', 'month': u'一月', 'forever': u'永久'}
#         users = UserInfo.objects.filter(type=2).order_by('-create_time')  # 类型为２的才是用户
#         for user in users:
#             ban_statue = u'正常'
#             if user.ban == 2:
#                 diff = (user.ban_time - datetime.datetime.now())
#                 if diff.seconds > 0:
#                     ban_statue = u'禁言(' + during_dict[user.ban_during] + '）'
#                 else:
#                     user.ban = 1
#                     user.save()
#             elif user.ban == 3:
#                 ban_statue = u'封禁'
#             user.ban_statue = ban_statue
#         return users



class UserInfoLogin(TemplateView):
    '''
    前端用户登录
    '''
    template_name = 'audience/login.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfoLogin, self).get_context_data(**kwargs)
        context['next'] = ''
        next = self.request.GET.get('next')
        if next:
            context['next'] = next
        return context

    def post(self, request):
        try:
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            code = request.POST.get('code')
            next = request.POST.get('next', None)

            user = authenticate(username=phone, password=password)
            if not user:
                # user 登录不成功，则换userinfo进行登录
                user_info_list = UserInfo.objects.filter(tel=phone)
                if not user_info_list:
                    messages.error(request, u'用户不存在')
                    return redirect('audience:login')

                user_info = user_info_list.first()
                if not code:
                    # 通过 手机 + 密码登录
                    if not check_password(password, user_info.passwd):
                        # 如果该方式检测不能成功登录，则使用自定义加密方式进行验证
                        password = user_info.user_id + settings.SECRET_KEY + password
                        password = hashlib.new('md5', password.encode("utf8")).hexdigest()
                        if password != user_info.passwd:
                            messages.error(request, u'用户名密码不匹配')
                            return redirect('audience:login')
                else:
                    # 通过 手机 + 验证码登录
                    memory_code = VerificationCode.get_code_by_phone(phone)
                    if memory_code != code:
                        messages.error(request, u'验证码不对')
                        return redirect('audience:login')
                user = user_info.owner

            # 判断完条件 则登录
            login(self.request, user)

            response = redirect('anchor:anchor_list')
            print next
            if next:
                response = redirect(next)
            return response

        except Exception as e:
            print str(e)
            return render(request, 'audience/login.html')


class ResetPasswordView(View):
    '''
    重置密码
    '''

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        code = request.POST.get('code')

        memory_code = VerificationCode.get_code_by_phone(phone)
        if memory_code != code:
            messages.error(request, u'验证码错误')
            return redirect('audience:login')

        user_info_list = UserInfo.objects.filter(tel=phone)
        if not user_info_list:
            messages.error(request, u'用户名不存在')
            return redirect('audience:login')

        user_info = user_info_list.first()
        user_info.passwd = make_password(password)
        user_info.save()

        # 更改完密码后直接登录
        user = user_info.owner
        login(self.request, user)

        response = redirect('anchor:anchor_list')
        return response


class VerificationCodeView(View):
    '''
    获取验证码
    '''

    def get(self, request, **kwargs):
        '''
        获取验证码

        1 注册 2 手机登录 3 第三方绑定 4 修改密码 5 修改手机号码
        CODE_REGISTRATION = '1'
        CODE_LOGIN = '2'
        CODE_BIND = '3'
        CODE_RESET_PASSWORD = '4'
        CODE_RESET_PHONE = '5'

        :param request:
        :return:
        '''
        phone = request.GET.get('phone', None)
        operate = request.GET.get('operate', CODE_REGISTRATION)
        user_info = UserInfo.objects.filter(tel=phone)

        # TODO 业务逻辑不清晰，待完善
        if operate == CODE_REGISTRATION:
            #  注册用户 获取验证码
            if user_info:
                return HttpResponse('该用户已存在', status=409)

        if operate in [CODE_LOGIN, CODE_RESET_PASSWORD]:
            # 已注册用户获取验证码
            if not user_info:
                return HttpResponse('用户不存在', status=404)

        result, code = VerificationCode.send_verification_code(phone)
        data = eval(result.text)
        if '25010' == data.get('code'):
            VerificationCode.save(phone, code)
            return HttpResponse(code, status=200)
        return HttpResponse('发送验证码失败，请稍后再试，谢谢！', status=500)


class Registration(View):
    '''
    注册

    检测手机号是否重复，但是检测为空的情况

    采用django 默认的加密方式

    user_info 需要存 user_id 字段，兼容老功能
    '''

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        code = request.POST.get('code')

        # 匹配验证码
        memory_code = VerificationCode.get_code_by_phone(phone)
        if memory_code != code:
            messages.error(request, '验证码错误')
            return redirect('audience:login')

        # 检测手机号
        if not phone:
            messages.error(request, '请输入手机号')
            return redirect('audience:login')

        user_info_list = UserInfo.objects.filter(tel=phone)
        if user_info_list:
            messages.error(request, '号码已经被注册使用')
            return redirect('audience:login')

        username = get_unique_username()
        with transaction.atomic():
            user = User.objects.create_user(username=username)
            owner = UserInfo(owner=user,  user_id=str(uuid.uuid1()).replace('-', ''), tel=phone, name=name, passwd=make_password(password))
            owner.save()

            login(self.request, user)

        response = redirect('anchor:anchor_list')
        return response
