# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from base.views import OwnerList
from .models import CourseInfo, LiveChannel, Channel
from anchor.models import AnchorInfo
from category.models import Category
from .utils import get_uuid

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
        else:
            post_data.pop('image')
        post_data.update({'course_id':get_uuid()})
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



@method_decorator(login_required, name='dispatch')
class LiveRoom(generic.DetailView):
    template_name = "course/live_room.html"
    context_object_name = "object"
    model = CourseInfo

    def get_context_data(self, **kwargs):
        '''
        方便以后添加其他信息
        '''
        context = super(LiveRoom, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, pk):
        self.object = self.get_object()
        print self.object,'======'
        context = self.get_context_data(object=self.object)
        context['object'] = self.object
        course_id=self.object.course_id
        #扩展点赞
        # context['support'] =support    
        channel_url = {'url_rtmp': '', 'url_flv': '', 'url_hls': '', 'pulish_url': '', 'status': ''}
        context['channel_url'] = channel_url
        live_channel = LiveChannel.objects.filter(video_id=course_id).first()
        if not live_channel:
            return context
        channel_info = Channel.objects.filter(pk=live_channel.channel_id).first()
        channel_url['url_rtmp'] = channel_info.url_rtmp
        channel_url['url_flv'] = channel_info.url_flv
        channel_url['url_hls'] = channel_info.url_hls
        channel_url['publish_url'] = channel_info.pulish_url
        channel_url['status'] = channel_info.status  
        print(channel_url,'=======') 
        return self.render_to_response(context)
 

   