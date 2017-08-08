# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from base.views import OwnerList
from category.models import Category
from course.models import CourseInfo
from anchor.models import AnchorInfo

@method_decorator(login_required, name='dispatch')
class IndexCategory(generic.ListView):
    template_name = "index/index.html"
    context_object_name = 'obj_list'

    def get_queryset(self):
        title = self.request.GET.get('title', None)
        object_list = Category.objects.all()
        if title:
            object_list = object_list.filter(name__icontains=title)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(IndexCategory, self).get_context_data(**kwargs)
        context['anchors'] = AnchorInfo.objects.filter(audit=1)
        return context

class IndexCourse(generic.ListView):
    template_name = "index/list.html"
    context_object_name = 'obj_list'

    def get_queryset(self):
        category_id = self.request.GET.get('category_id', None)
        object_list = CourseInfo.objects.filter(audit=1)
        if category_id:
            object_list = object_list.filter(category_id=category_id)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(IndexCourse, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['Anchors'] = AnchorInfo.objects.filter(audit=1)
        return context