# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^anchor/', include('anchor.urls', namespace="anchor")),
    url(r'^course/', include('course.urls', namespace="course")),
    url(r'^category/', include('category.urls', namespace="category")),
    url(r'^audience/', include('audience.urls', namespace="audience")),
    url(r'^management/', include('management.urls', namespace="management")),
    url(r'^index/', include('index.urls', namespace="index")),




    #直播api
    url(r'^courses/', include('course.api_urls')),
    url(r'^categories/', include('category.api_urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
