# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib.auth.views import logout_then_login, password_change

from . import views



urlpatterns = [
    # 前端用户
    url(r'^management_list/$', views.AuthList.as_view(), name='management_list'),
    url(r'^management_add/$', views.AuthAdd.as_view(), name='management_add'),
    # url(r'^management_edit/(?P<pk>\w*)/$', views.AnchorEdit.as_view(), name='management_edit'),
    url(r'^logout/$', logout_then_login, name='logout'),


]
