# coding: utf-8
import random
import datetime
import string
import time
import hmac
import base64
import hashlib
import urllib
import oss2, sys
import os
import hashlib
from itertools import islice
from django.conf import settings
from public.utils import get_url
import logging
from celery import shared_task


import os
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo

logger = logging.getLogger('aliyun')


def get_signature_string(params):
    """
    根据aliyun提供步骤，得到加密串
    """
    # 排序
    param_items = list(params.items())
    param_items.sort()

    # url encode
    _n_param = []
    for key, val in param_items:
        key = urllib.urlencode({"k": key}).split("=", 1)[1]
        val = urllib.urlencode({"k": val}).split("=", 1)[1]

        _n_param.append([key, val])

    # urlencode
    _str = ["%s=%s" % (key, val) for key, val in _n_param]
    _encode_str = "&".join(_str)

    # url / parse
    _parse = urllib.urlencode({"k": "/"}).split("=", 1)[1]

    _encode_str = urllib.urlencode({"key": _encode_str}).split("=", 1)[1]

    # 加入GET&/&
    encode_str = "GET&" + _parse + "&" + _encode_str
    return encode_str


def aliyun_sgin(secret, encode_str):
    # hmac
    key = bytes(secret)
    message = bytes(encode_str)
    digester = hmac.new(key, msg=message, digestmod=hashlib.sha1)
    signature1 = digester.digest()
    # sha1
    signature2 = base64.b64encode(signature1)
    return str(signature2)


def nowtime():
    """
    当前时间戳
    """
    return str(time.time()).replace(".", "")


def utc_nowtime():
    """
    当前utc时间
    """
    _format = "%Y-%m-%dT%H:%M:%SZ"
    _now = datetime.datetime.utcnow()
    return _now.strftime(_format)


def timestamp2utc(timestamp=None):
    """
    时间戳转utc
    """
    if not timestamp:
        timestamp = time.time()
    utc = datetime.datetime.utcfromtimestamp(timestamp)
    return utc


def timestamp2utc_string(timestamp=None, _format="%Y-%m-%dT%H:%M:%SZ"):
    """
    时间戳根据format转utc字符串
    """
    utc = timestamp2utc(timestamp)
    utc_string = utc.strftime(_format)
    return utc_string


def datetimestr2utcstr(datetime_str, _format="%Y-%m-%dT%H:%M:%SZ"):
    """
    时间字符串转换成utc字符串
    """
    # 转换成时间对象
    _d_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    _timestamp = time.mktime(_d_time.utctimetuple())
    # 得到utc时间对象
    _utc_d_time = datetime.datetime.utcfromtimestamp(_timestamp)
    # 转换成utc字符
    utc_string = _utc_d_time.strftime(_format)
    return utc_string


def datatime_to_str(datatime, format="%Y-%m-%dT%H:%M:%SZ"):
    """
    时间字符串转换成utc字符串
    """
    # 转换成时间戳
    timestamp = time.mktime(datatime.utctimetuple())
    # 得到utc时间对象
    utc_d_time = datetime.datetime.utcfromtimestamp(timestamp)
    # 转换成utc字符
    utc_string = utc_d_time.strftime(format)
    return utc_string


def datetime2string(d_time=None, _format="%Y-%m-%d %H:%M:%S"):
    if not d_time:
        d_time = datetime.datetime.now()
    return d_time.strftime(_format)


def nonce(data=None):
    """
    得到随机字符串
    """
    if not data:
        data = string.ascii_letters
    nonce_list = [random.choice(data) for x in range(14)]
    nonce = "".join(nonce_list)
    return nonce


def aliyun_oss():
    auth = oss2.Auth(settings.ALIYUN_ACCESS_KEY, settings.ALIYUN_SECRET[:-1])
    bucket = oss2.Bucket(auth, settings.ALIYUN_OSS_ENDPOINT, settings.ALIYUN_OSS_BUCKET)
    return bucket


# 文件资源上传阿里云
def file_to_oss(id, file, type_name='courses'):
    file_name = ''
    if file:
        _, file_ext = os.path.splitext(file.name)
        md = hashlib.md5()
        md.update((str(time.time()) + file.name).encode('utf8'))
        # type_name in ('image','video','audio',...) 对应oss 管理的目录名
        bucket = aliyun_oss()
        file_name = type_name + '/' + str(id) + '/' + md.hexdigest() + file_ext

        oss_file_name = os.path.join(settings.ALIYUN_OSS_DIRECTORY_PREFIX, file_name)
        bucket.put_object(oss_file_name, file)
    return file_name

def oss_path(id, file_name=None, type_name='course_record'):

    relative_path = type_name + '/' + str(id) + '/'
    absolute_path = os.path.join(settings.ALIYUN_OSS_DIRECTORY_PREFIX, relative_path)
    if file_name:
        relative_path = file_name.replace(settings.ALIYUN_OSS_DIRECTORY_PREFIX, '')
    return {'relative_path': relative_path, 'absolute_path': absolute_path}


def bytes_to_oss(id, bytes, type_name='courses'):
    '''
    字节流直接存入文件
    :param id:
    :param bytes:
    :param type_name:
    :return:
    '''
    file_name = ''
    if bytes:
        md = hashlib.md5()
        md.update(str(time.time()).encode('utf8'))
        # type_name in ('image','video','audio',...) 对应oss 管理的目录名
        bucket = aliyun_oss()
        file_name = type_name + '/' + str(id) + '/' + md.hexdigest()

        oss_file_name = os.path.join(settings.ALIYUN_OSS_DIRECTORY_PREFIX, file_name)
        bucket.put_object(oss_file_name, bytes)
    return file_name


def list_record(name):
    bucket = aliyun_oss()
    list = []
    prefix = os.path.join(settings.ALIYUN_OSS_DIRECTORY_PREFIX, 'record', name)
    logger.info(prefix)
    for b in oss2.ObjectIterator(bucket, prefix=prefix):
        list.append(os.path.join(settings.ALIYUN_OSS_CDN_URL, b.key))
    return list

#todo进度条
# def percentage(consumed_bytes, total_bytes):
#     if total_bytes:
#         rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
#         print('\r{0}% '.format(rate), end='')
#         sys.stdout.flush()

def get_oss_file_path(id, file, type_name='courses'):
    file_name = ''
    if file:
        _, file_ext = os.path.splitext(file.name)
        md = hashlib.md5()
        md.update((str(time.time()) + file.name).encode('utf8'))
        file_name = type_name + '/' + str(id) + '/' + md.hexdigest() + file_ext
    return file_name

@shared_task
def large_file_to_oss(id, file, type_name='courses'):
    try:
        file_name = ''
        if file:
            _, file_ext = os.path.splitext(file.name)
            md = hashlib.md5()
            md.update((str(time.time()) + file.name).encode('utf8'))
            file_name = type_name + '/' + str(id) + '/' + md.hexdigest() + file_ext
            oss_file_name = os.path.join(settings.ALIYUN_OSS_DIRECTORY_PREFIX, file_name)
            bucket = aliyun_oss()
            key = oss_file_name
            filename = file
            total_size = filename.size
            part_size = determine_part_size(total_size, preferred_size=100 * 1024)
            # 初始化分片
            upload_id = bucket.init_multipart_upload(key).upload_id
            parts = []
            # 逐个上传分片
            part_number = 1
            offset = 0
            while offset < total_size:
                num_to_upload = min(part_size, total_size - offset)
                result = bucket.upload_part(key, upload_id, part_number,
                                            SizedFileAdapter(file, num_to_upload))
                parts.append(PartInfo(part_number, result.etag))
                offset += num_to_upload
                part_number += 1
            # 完成分片上传
            bucket.complete_multipart_upload(key, upload_id, parts)
            # # 验证一下
            #
            # assert bucket.get_object(key).read() == file.read()
        return file_name
    except Exception:
        logger.error("Exceptions: {}".format(sys.exc_info()[0]))
