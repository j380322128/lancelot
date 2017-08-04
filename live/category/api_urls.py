# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', api.CategoryViewSet)

urlpatterns = [

    # API 接口

    url(r'^', include(router.urls)),
]
