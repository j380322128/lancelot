# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import  views

urlpatterns = [
    # 前端用户
    url(r'^course_list/$', views.CourseList.as_view(), name='course_list'),
    url(r'^course_add/$', views.CourseAdd.as_view(), name='course_add'),
    url(r'^course_edit/(?P<pk>\w*)/$', views.CourseEdit.as_view(), name='course_edit'),
    url(r'^course_audit/$', views.audit, name='course_audit'),

  	#直播地址
    url(r'^live_room/(?P<pk>\w*)/$', views.LiveRoom.as_view(), name='live_room'),

]
