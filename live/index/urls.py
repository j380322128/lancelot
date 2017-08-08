# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views



urlpatterns = [
    # 分类
    url(r'^index_category/$', views.IndexCategory.as_view(), name='index_category'),
    url(r'^courses/$', views.IndexCourse.as_view(), name='courses'),

]