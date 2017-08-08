# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from base.views import OwnerList
from .models import CourseInfo
from anchor.models import AnchorInfo
from category.models import Category

@method_decorator(login_required, name='dispatch')
class CourseList(generic.ListView):
    template_name = 'course/course_list.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title:
            object_list = CourseInfo.objects.filter(title__icontains=title)  
        else:
            object_list = CourseInfo.objects.all()
        return object_list


@method_decorator(login_required, name='dispatch')
class CourseAdd(generic.TemplateView):
    template_name = "course/course_add.html"

    def get_context_data(self, **kwargs):
        context = super(CourseAdd, self).get_context_data(**kwargs)
        context['user'] = AnchorInfo.objects.all()
        context['categories'] = Category.objects.all()
        return context

    def post(self, request):
        post_data = request.POST
        post_file = request.FILES
        image = post_file.get('image', None)
        if image:
            post_data.update({'image': image})

        save_data = {key: val for key, val in post_data.items() if val and key in dir(CourseInfo)}
        anchor_info = CourseInfo(**save_data)
        anchor_info.save()
        return redirect("course:course_list")

@method_decorator(login_required, name='dispatch')
class CourseEdit(generic.DetailView):
    template_name = "course/course_add.html"
    model = CourseInfo
    queryset = CourseInfo.objects.all()

    def get_context_data(self, **kwargs):
        '''
        方便以后添加其他信息
        '''
        context = super(CourseEdit, self).get_context_data(**kwargs)
        context['user'] = AnchorInfo.objects.all()
        context['categories'] = Category.objects.all()
        
        return context

    def get(self, request, pk):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['object'] = self.object
        context['action'] = "/course/course_edit/{}/".format(pk)
        return self.render_to_response(context)

    def post(self, request, pk):
        post_data = request.POST
        post_file = request.FILES
        image = post_file.get('image', None)
        if image:
            post_data.update({'image': image})
        course = CourseInfo.objects.get(pk=pk)

        for key, val in post_data.items():
            if not val:
                post_data.pop(key)
                continue
            if hasattr(course, key):
                setattr(course, key, val)
        course.save()
        return redirect("course:course_list")

@csrf_exempt
def audit(req):
    post_data = req.POST
    audit = post_data.get('audit', None)
    id = post_data.get('id', None)
    course = CourseInfo.objects.get(pk=id)
    course.audit = audit
    course.save()
    return JsonResponse({'result': 'success', 'message': u'修改成功'})
