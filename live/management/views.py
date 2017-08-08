# -*- coding: utf-8 -*-
import os
import uuid
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, FormView, TemplateView, DetailView, View
from django.contrib.auth import authenticate, logout, login
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

from audience.models import UserInfo

from base.views import OwnerList
from audience.utils import get_unique_username


@method_decorator(login_required, name='dispatch')
class AuthList(OwnerList):
    template_name = 'management/list.html'
    context_object_name = 'obj_list'
    model_class = UserInfo
    form_fields = []
    # 默认查询，为提供同一个表根据不同的默认条件获取不同意义的数据
    default_filters = {}
    request_key = ["tel", "name"]

    def get_queryset(self):
        # handler_history()
        user = self.request.user
        object_list = super(AuthList, self).get_queryset()
        return object_list


@method_decorator(login_required, name='dispatch')
class AuthAdd(generic.TemplateView):
    template_name = "management/management_add.html"

    def post(self, request):
        post_data = request.POST
        user_id=str(uuid.uuid1()).replace('-', '')
        post_data.update({'user_id': user_id})

        username = get_unique_username()
        with transaction.atomic():

            user = User.objects.create_user(username=username, is_staff=1)
            post_data.update({'owner': user, 'type':1})
            save_data = {key: val for key, val in post_data.items() if val and key in dir(UserInfo)}
            owner = UserInfo(**save_data)            
            owner.save()
        return redirect("management:management_list")

class LoginForm(FormView):
    '''
    后台登录
    '''
    template_name = 'management/login.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super(LoginForm, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.POST.get('next', None)

            user = authenticate(username=username, password=password)
            if not user:
                messages.error(request, u'用户名密码不匹配')
                return redirect('management:login')

            if not user.is_superuser and not user.is_staff:
                messages.error(request, u'权限不足，不能登录后台')
                return render(request, 'management/login.html')
    
            if next:
                    response = redirect(next)
            else:
                response = redirect('anchor:anchor_list')
      
            login(self.request, user)
            
            return response

        except Exception as e:
            messages.error(request, u'用户名或者密码错误')
            return render(request, 'management/login.html')