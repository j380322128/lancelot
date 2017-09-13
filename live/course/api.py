# -*- coding: utf-8 -*-
# Create your views here.
import json
import os
import sys
import urllib
import uuid
import traceback
import logging
import time
from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import (NotFound, ParseError, PermissionDenied, APIException)
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status as HTTPStatus

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from public.utils import InternalServerError, ServiceConflict, ServiceUnavailable
from aliyun.aliyunsdk import AliyunLiveClient
from aliyun.utils import datatime_to_str
from public.utils import datetime2string, WEEKDAY_DICT
from aliyun.utils import file_to_oss
from .utils import datetime2time, string2datetime, datetime2string, get_uuid



from aliyun.utils import (
    nowtime,
    utc_nowtime,
    timestamp2utc,
    timestamp2utc_string,
    datetimestr2utcstr,
)
from aliyun.aliyun_request import ClientException
from audience.models import (
    UserInfo)
from .serializers import CourseSerializer
from .models import (CourseInfo, LiveChannel, Channel, LIVE_STATUS_ON,
                     LIVE_STATUS_OVER, RECORD_STATUS_NO, RECORD_STATUS_HAVE, 
                     COURSE_LIVE, COURSE_RESERVATION, COURSE_OVER, COURSE_REPLAY,
                     RESOURCE_ULLGET)

from public.check_permission import AdminPermission, StaffPermission, IsOwnerOrReadOnly, \
    StarPermission, StarOrStaffPermission


logger = logging.getLogger('apps')

CHECK_COURSE = "course"
CHECK_SERIES = "series"
CHECK_TYPE_CHOICES = (
    (CHECK_COURSE, "检查课程"),
    (CHECK_SERIES), "检查系列课")

DEFAULT_USER = 'default/default_user.png'
class CourseViewSet(viewsets.ModelViewSet):
    # """
    # 这一viewset提供了`list`, `create`, `retrieve`, `update` 和 `destroy`
    # """

    queryset = CourseInfo.objects.filter(active=1)
    serializer_class = CourseSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('user_id', 'series_id')

    permission_classes_by_action = {
        'default': [AllowAny]
        # 'list': [AllowAny],
        # 'retrieve': [AllowAny],
        # 'courses_sort': [AllowAny],
        # 'recommended_courses_detail': [AllowAny],
        # 'live_num': [IsAuthenticatedOrReadOnly],
        # 'cumulative_num': [AllowAny],
        # 'default': [StarOrStaffPermission],
        # 'forbidden_or_resume_pulish_stream': [StarOrStaffPermission],
        # 'course_record': [StarOrStaffPermission],
        # 'recourd_url': [StarOrStaffPermission],
        # 'owner': [IsAuthenticatedOrReadOnly],
        # 'buy_course': [IsAuthenticatedOrReadOnly],
        # 'like': [IsAuthenticatedOrReadOnly],
        # 'interesting': [IsAuthenticatedOrReadOnly],
        # 'recommended_courses': [IsAuthenticatedOrReadOnly],
        # 'series': [IsAuthenticatedOrReadOnly],
        # 'blacklist': [StaffPermission],
        # 'courses_by_keyword':[IsOwnerOrReadOnly],
        # 'make_poster_image': [],
        # 'course_settings': []
        }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]

    def split_url_rtmp(self, url_rtmp):
        data = url_rtmp[7:].split('/')
        return data

    def get_object(self):
        """
        详情
        重写父类，方便返回详情加入是否购买，点赞etc.. 这有客户端不需要到这个页面同时访问多个接口
        """
        obj = super(CourseViewSet, self).get_object()
        obj.bought = 0  # 默认未购买
        obj.like = 0  # 默认未点赞

        user = self.request.user
        # 如果有登录，判断是否购买此课程
        if not isinstance(user, AnonymousUser):
            if MyCourse.objects.filter(owner_user=user, course=obj).exists():
                obj.bought = 1
        return obj




    @detail_route()
    def live_num(self, request, pk=None):
        '''
        获取直播在线人数
        '''
        video_info = CourseInfo.objects.filter(id=pk).first()
        if not video_info:
            raise NotFound(detail='直播不存在')

        live_info = LiveChannel.objects.filter(video_id=video_info.course_id).first()
        if not live_info:
            raise NotFound(detail='直播未开始')

        channel_info = Channel.objects.filter(id=live_info.channel_id).first()
        if channel_info.url_rtmp:
            cdn_domain, app_name, stream_name = self.split_url_rtmp(channel_info.url_rtmp)
        else:
            raise NotFound(detail='直播流地址不存在')

        start_time = video_info.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        client = AliyunLiveClient()
        respones = client.get_live_stream_online_user_num(cdn_domain, app_name, stream_name, start_time)

        OnlineUserInfo = respones.get('OnlineUserInfo', None)
        if OnlineUserInfo:
            LiveStreamOnlineUserNumInfo = OnlineUserInfo.get('LiveStreamOnlineUserNumInfo', None)
            if LiveStreamOnlineUserNumInfo:
                for live in LiveStreamOnlineUserNumInfo:
                    if live.get('StreamUrl') == channel_info.url_rtmp:
                        num = live.get('UserNumber')
                        return Response({'result': 'success', 'message': num}, status=status.HTTP_200_OK)

        raise ServiceUnavailable(detail='获取在线人数调用失败')


    @list_route(methods=['post'])
    def recourd_url(self, request):
        '''
        获取录播地址
        '''

        id = request.POST.get('id')
        video_info = CourseInfo.objects.filter(pk=id).first()
        if not video_info:
            raise NotFound(detail='录播不存在')

        live_info = LiveChannel.objects.filter(video_id=video_info.course_id).first()
        if not live_info:
            raise NotFound(detail='该直播课没有直播，录播不存在 ')

        channel = Channel.objects.filter(id=live_info.channel_id).first()
        if channel.url_rtmp:
            cdn_domain, app_name, stream_name = self.split_url_rtmp(channel.url_rtmp)
        else:
            raise NotFound(detail='录播不存在')

        start_time = datatime_to_str(video_info.start_time)
        # 结束i日期往后放大1天
        end_time = datatime_to_str(video_info.end_time + timedelta(days=1))
        client = AliyunLiveClient()
        try:
            record_list = client.get_live_stream_record_index_files(cdn_domain, app_name, stream_name, start_time,
                                                                    end_time)
        except ClientException as client_except:
            raise NotFound(detail="没有可以生成录播的流")

        record_list = record_list.get('RecordIndexInfoList', None)
        if record_list:
            if record_list.get('RecordIndexInfo', None):
                record_info = record_list.get('RecordIndexInfo', None)[0]
                if settings.ALIYUN_OSS_DIRECTORY_PREFIX in record_info['RecordUrl']:
                    record_url = \
                        record_info['RecordUrl'].split('com')[1].split(settings.ALIYUN_OSS_DIRECTORY_PREFIX)[1]
                else:
                    record_url = record_info['RecordUrl'].split('com/')[1]
                video_info.url = record_url
                video_info.status = COURSE_REPLAY
                video_resource = RESOURCE_ULLGET
                video_info.save()
            else:
                raise NotFound(detail='录播正在生成中')
        else:
            raise ServiceUnavailable(detail='生成录播出错')
        return Response({'result': 'success', 'message': record_list}, status=status.HTTP_200_OK)

   
    @detail_route()
    def course_record(self, request, pk=None):
        '''
        课程设置录播配置
        '''
        video_info = CourseInfo.objects.get(pk=pk)
        appname = str(video_info.id) + '_' + video_info.course_id
        result = ''
        try:
            result = AliyunLiveClient().add_live_app_record_config(settings.ALIYUN_LIVE_CDN_DOMAIN, appname,
                                                                   settings.ALIYUN_OSS_BUCKET,
                                                                   settings.ALIYUN_OSS_DIRECTORY_PREFIX + 'record',
                                                                   'mp4'
                                                                   )
        except Exception as e:
            if 'ConfigAlreadyExists' in e.args[0]:
                return Response({'result': 'fail', 'message': '录播配置已打开'}, status=status.HTTP_200_OK)
            else:
                logger.error(u'打开录播配置出错  ' + str(e))
                raise ServiceUnavailable(detail='打开录播配置出错')
        return Response({'result': 'success', 'message': result}, status=status.HTTP_200_OK)

    @detail_route()
    def course_delete_record(self, request, pk=None):
        '''
        课程删除录播配置
        '''
        video_info = CourseInfo.objects.get(pk=pk)
        appname = str(video_info.id) + '_' + video_info.course_id
        result = AliyunLiveClient().delete_live_app_record_config(settings.ALIYUN_LIVE_CDN_DOMAIN, appname)
        return Response({'result': 'success', 'message': result}, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def forbidden_or_resume_pulish_stream(self, request):
        option = request.POST.get('option')
        id = request.POST.get('id')
        if option not in ('forbidden', 'resume'):
            raise ParseError(detail='非法参数')
        video_info = CourseInfo.objects.filter(pk=id).first()
        if not video_info:
            raise NotFound(detail='直播不存在')

        live_info = LiveChannel.objects.filter(video_id=video_info.course_id).first()
        if option == 'resume':
            # 开始时间，以老师直播端点击对应按钮为准
            if not live_info:
                client = AliyunLiveClient()
                stream_name = ''
                appname = str(video_info.id) + '_' + video_info.course_id

                record_status = RECORD_STATUS_NO

                # 生成录播的直播与不生成录播的区分开
                if video_info.live_to_record == 1:
                    record_status = RECORD_STATUS_HAVE

                # 正在直播流的数量
                channel_num = Channel.objects.filter(appname=appname, status=LIVE_STATUS_ON).count()
                if channel_num >= 10:
                    raise PermissionDenied(detail='您创建的直播数不能超过10个')

                # 目前阿里云不支持实时转码
                # #添加转码配置
                # transcode = client.live_stream_transcode(settings.ALIYUN_LIVE_CDN_DOMAIN, appname)
                # if not transcode.get('RequestId', None):
                #     raise ServiceUnavailable(detail='添加转码配置失败')

                # 创建直播流
                url = client.create_channel(appname)
                stream_info = url.get('pull_rtmp', None)
                if stream_info:
                    stream_name = stream_info[7:].split('/')[2]
                    url_pulish_url = url.get('pulish_url')
                    url_pull_rtmp = url.get('pull_rtmp')
                    url_pull_flv = url.get('pull_flv').replace('http', 'https')
                    url_pull_hls = url.get('pull_hls').replace('http', 'https')
                    with transaction.atomic():
                        new_channel = Channel.objects.create(pulish_url=url_pulish_url,
                                                             url_rtmp=url_pull_rtmp,
                                                             url_flv=url_pull_flv,
                                                             url_hls=url_pull_hls,
                                                             record_status=record_status, appname=appname,
                                                             status=LIVE_STATUS_ON)
                        live_channel = LiveChannel.objects.create(video_id=video_info.course_id, channel=new_channel,
                                                                  status=LIVE_STATUS_ON, stream_name=stream_name)
                        video_info.status = 1
                        video_info.save()
                        get_urls = {
                            'url_rtmp': url_pull_rtmp,
                            'url_flv': url_pull_flv,
                            'url_hls': url_pull_hls,
                        }
                    return Response({'result': 'success', 'message': 'success_to_create_live', 'live_channel_id': live_channel.id,
                                     'publish_url': url.get('pulish_url'), 'get_url': get_urls, 'status':LIVE_STATUS_ON},
                                    status=status.HTTP_200_OK)
                else:
                    raise ServiceUnavailable(detail='创建直播流失败')
            else:
                if video_info.status == COURSE_REPLAY:
                    raise ServiceConflict(detail='该课程直播已结束')

                channel_info = Channel.objects.filter(id=live_info.channel_id).first()

                if channel_info and channel_info.status == LIVE_STATUS_ON:
                    raise ServiceConflict(detail='该课程正在直播')

                if channel_info.url_rtmp:
                    cdn_domain, app_name, stream_name = self.split_url_rtmp(channel_info.url_rtmp)
                else:
                    raise NotFound(detail='直播流不存在')

                client = AliyunLiveClient()
                respones = client.forbidden_or_resume_pulish_stream(cdn_domain, app_name, stream_name, option)
                if respones.get('RequestId'):
                    with transaction.atomic():
                        channel_info.status = LIVE_STATUS_ON
                        channel_info.save()
                        live_info.status = LIVE_STATUS_ON
                        live_info.save()
                        if live_info.stream_status != 'test':
                            video_info.start_time = datetime2string(datetime.now())
                        video_info.status = 1
                        video_info.save()
                        get_urls = {
                            'url_rtmp': channel_info.url_rtmp,
                            'url_flv': channel_info.url_flv,
                            'url_hls': channel_info.url_hls
                        }
                    return Response({'result': 'success', 'message': respones, 'live_channel_id': live_info.id,
                                     'publish_url': channel_info.pulish_url, 'get_url': get_urls, 'status':LIVE_STATUS_ON},
                                    status=status.HTTP_200_OK)
                else:
                    raise ServiceUnavailable(detail='调用失败')
        else:
            if not live_info:
                raise ServiceConflict(detail='该课程还未开始直播')

            # 结束时间，以老师直播端点击对应按钮为准
            if live_info.stream_status != 'test':
                video_info.end_time = datetime2string(datetime.now())

            client = AliyunLiveClient()
            channel_info = Channel.objects.filter(id=live_info.channel_id).first()

            if channel_info and channel_info.status == LIVE_STATUS_OVER:
                raise ServiceConflict(detail='直播已结束')

            if channel_info.url_rtmp:
                cdn_domain, app_name, stream_name = self.split_url_rtmp(channel_info.url_rtmp)
            else:
                raise InternalServerError(detail='直播流地址不存在')

            respones = client.forbidden_or_resume_pulish_stream(cdn_domain, app_name, stream_name, option)

            if respones.get('RequestId'):
                with transaction.atomic():
                    channel_info.status = LIVE_STATUS_OVER
                    channel_info.save()
                    live_info.status = LIVE_STATUS_OVER
                    live_info.save()
                    video_info.status = 3
                    video_info.save()
                return Response({'result': 'success', 'message': respones, 'live_channel_id': live_info.id, 'status':LIVE_STATUS_OVER},
                                status=status.HTTP_200_OK)
            else:
                raise ServiceUnavailable(detail='调用失败')

   

   


