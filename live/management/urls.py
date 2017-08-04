# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views



urlpatterns = [
    # 前端用户
    url(r'^management_list/$', views.AuthList.as_view(), name='management_list'),
    # url(r'^management_add/$', views.AnchorAdd.as_view(), name='management_add'),
    # url(r'^management_edit/(?P<pk>\w*)/$', views.AnchorEdit.as_view(), name='management_edit'),

]
