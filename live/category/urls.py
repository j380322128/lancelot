# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views



urlpatterns = [
    # 分类
    url(r'^category_list/$', views.CategoryList.as_view(), name='category_list'),
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),


]
