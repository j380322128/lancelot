# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import  views

urlpatterns = [
    # 前端用户
    url(r'^course_list/$', views.CourseList.as_view(), name='course_list'),
    # url(r'^anchor_add/$', views.AnchorAdd.as_view(), name='anchor_add'),
    # url(r'^anchor_edit/(?P<pk>\w*)/$', views.AnchorEdit.as_view(), name='anchor_edit'),
    # url(r'^anchor_audit/$', views.audit, name='anchor_audit'),

]
