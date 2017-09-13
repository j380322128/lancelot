# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from raven.contrib.django.raven_compat.models import client
from rest_framework.pagination import PageNumberPagination


import re
import random
import json
import os
import sys
import requests

sys.path += ["/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python"]

import six
import time
from hashlib import sha1, md5

from xml.etree import ElementTree

from datetime import datetime, timedelta
from time import time, mktime, strftime, localtime
import logging

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    client.captureException()
    logging.exception(exc)
    # Now add the HTTP status code to the response.
    # if response is not None:
    #     # response.data['status_code'] = exc
    #     response.data['detail'] = exc.args[0]

    return response


class InternalServerError(APIException):
    status_code = 500
    default_detail = 'INTERNAL_SERVER_ERROR.'
    default_code = 'internal_server_error'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'SERVICE_UNAVAILABLE'
    default_code = 'service_unavailable'


class ServiceConflict(APIException):
    status_code = 409
    default_detail = 'CONFLICT_SERVER_ERROR.'
    default_code = 'service_conflict'


#重写的自定义的分页类，给特例的api使用
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000



def get_url(path):
    '''
    拼接url，在前台呈现
    :param path:
    :return:
    '''
    if not path or path.startswith("http"):
        return path
    return os.path.join(settings.ALIYUN_OSS_CDN_URL,
                        settings.ALIYUN_OSS_DIRECTORY_PREFIX,
                        path)


string_types = (six.string_types, six.text_type, six.binary_type)


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def to_text(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding="utf-8"):
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


def is_string(value):
    return isinstance(value, string_types)


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    token = []
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    for _ in range(length):
        token.append(random.choice(letters))
    return ''.join(token)


def dict_parse_from_xml(xml_data):
    json = dict((child.tag, to_text(child.text))
                for child in ElementTree.fromstring(xml_data))
    return json


def dict_parse_to_xml(dict):
    xml = ""
    for key, val in dict.iteritems():
        xml += "<{0}>{1}</{0}>".format(key, val)
    return xml


def datetime2time(d_time):
    if not d_time:
        return 0
    return int(mktime(d_time.timetuple()))


def timestamp2string(timestamp):
    if (not timestamp) or (not isinstance(timestamp, int)):
        return timestamp
    return strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp))


def datetime2string(d_time=None, _format="%Y-%m-%d %H:%M:%S"):
    if not d_time:
        d_time = datetime.now()
    return d_time.strftime(_format)


def string2datetime(string, _format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(string, _format)


def generator_code(length=6):
    letters = "0123456789"
    code = "".join(random.sample(letters, length))
    return code


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def lookup_ip(ip):
    """
    根据ip得到地址信息
    """
    url = "http://ip.taobao.com/service/getIpInfo.php"

    querystring = {"ip": ip}
    response = requests.request("GET", url, params=querystring)

    return response.json()

WEEKDAY_DICT = {
    0: "周一",
    1: "周二",
    2: "周三",
    3: "周四",
    4: "周五",
    5: "周六",
    6: "周天"
}

