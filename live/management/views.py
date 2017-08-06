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
from django.db import transaction

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


# @method_decorator(login_required, name='dispatch')
# class AnchorEdit(generic.DetailView):
#     template_name = "management/management_add.html"
#     model = AnchorInfo
#     queryset = AnchorInfo.objects.all()

#     def get_context_data(self, **kwargs):
#         '''
#         方便以后添加其他信息
#         '''
#         context = super(AnchorEdit, self).get_context_data(**kwargs)
#         return super(AnchorEdit, self).get_context_data(**context)

#     def get(self, request, pk):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         context['object'] = self.object
#         context['action'] = "/anchor/anchor_edit/{}/".format(pk)
#         return self.render_to_response(context)

#     def post(self, request, pk):
#         post_data = request.POST
#         post_file = request.FILES
#         image = post_file.get('image', None)
#         if image:
#             post_data.update({'image': image})
#         anchor = AnchorInfo.objects.get(pk=pk)

#         for key, val in post_data.items():
#             if hasattr(anchor, key):
#                 setattr(anchor, key, val)
#         anchor.save()
#         return redirect("anchor:anchor_list")

# @csrf_exempt
# def audit(req):
#     post_data = req.POST
#     audit = post_data.get('audit', None)
#     id = post_data.get('id', None)
#     anchor = AnchorInfo.objects.get(pk=id)
#     anchor.audit = audit
#     anchor.save()
#     return JsonResponse({'result': 'success', 'message': u'修改成功'})
