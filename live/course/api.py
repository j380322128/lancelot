# -*- coding: utf-8 -*-

import os
import sys
import urllib
import uuid
import traceback
import logging
import hmac
from datetime import datetime, timedelta
import base64
from hashlib import sha1

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
from .serializers import CourseSerializer
from .models import CourseInfo


class CourseViewSet(viewsets.ModelViewSet):
    # """
    # 这一viewset提供了`list`, `create`, `retrieve`, `update` 和 `destroy`
    # """

    queryset = CourseInfo.objects.filter(active=1)
    serializer_class = CourseSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

