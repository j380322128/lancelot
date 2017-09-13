# -*- coding: utf-8 -*-
import random
import time
from time import mktime, strftime, localtime
from hashlib import sha1, md5

from xml.etree import ElementTree

from datetime import datetime

import uuid
from .models import CourseInfo
import logging
from .models import LiveChannel, COURSE_LIVE , COURSE_RESERVATION ,COURSE_OVER ,COURSE_REPLAY,COURSE_LIVE_NOUSER

logger = logging.getLogger('apps')


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


def set_chatroom(activity_id, lean_id):
    # 将chatroom存入数据库
    video_info = VideoInfo.objects.filter(course_id=activity_id)
    if video_info:
        video_item = video_info.first()
        video_item.chat_room_id = lean_id
        video_item.save()
        return True
    return False


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


def timestamp2string(timestamp, _format="%Y-%m-%d %H:%M:%S"):
    if (not timestamp) or (not isinstance(timestamp, int)):
        return timestamp
    return strftime(_format, localtime(timestamp))


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


def get_total_page(total, page_size):
    number = total / page_size if not total % page_size else total / page_size + 1
    return number


def get_limit_paging(current_page, page_size=12):
    """
    得到分页开始和结束
    """
    current_page, page_size = int(current_page), int(page_size)
    _start = (current_page - 1) * page_size
    _end = current_page * page_size
    return _start, _end


def get_view_time(timestamp):
    """
    得到前台显示评论相关时间
    1分钟以内为“刚刚”，1分钟到1个小时“1分钟前”，1个小时到一天为“1小时前”，一天到三十天为“一天前”，三十天以上显示“一个月前”。
    """
    _now_time = int(time())
    if _now_time >= timestamp:
        _passed = _now_time - timestamp
        # 转换为分
        _passed = _passed / 60

        if _passed < 1:
            # 刚刚
            return "刚刚"
        elif _passed >= 1 and _passed <= 60:
            # 1分钟到1个小时
            return "1分钟前"
        elif _passed >= 60 and _passed <= 60 * 24:
            # 1小时前
            return "1小时前"
        elif _passed >= 60 * 24 and _passed <= 60 * 24 * 30:
            # 一天前
            return "一天前"
        elif _passed >= 60 * 24 * 30:
            # 一个月前
            return "一个月前"
        else:
            return "未知"


def get_sign(kwargs, sign_type='MD5', pay_sign_key=None, is_upper=True):
    """
    微信签名参数组装
    @param: params 参与签名的参数
    @param: sign_type 签名类型
    @param: pay_sign_key 是否需要支付密钥
    @return: sign, sign_type
    """
    # 根据ascii码进行排序
    params = kwargs.items()
    params.sort()
    # urle拼接
    string = "&".join(["%s=%s" % (str(p[0]), str(p[1])) for p in params])
    if pay_sign_key:
        string += "&key=%s" % pay_sign_key
    # 生成签名 Point: 这里签名时间戳，必须与wxconfig中得时间戳一致---坑呀
    if sign_type == "MD5":
        sign = md5(string).hexdigest().upper() if is_upper else md(string).hexdigest()
    if sign_type == "SHA1":
        sign = sha1(string).hexdigest().upper() if is_upper else sha1(string).hexdigest()
    return sign, sign_type


def out_trade_no(pid):
    _out_trade_no = str(time()).replace(".", "") + str(pid)
    logger.info(_out_trade_no)

    return _out_trade_no[:32]


def make_object_no(object_type):
    """
    生成对象编号
    """
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    _id = object_type + "".join(random.sample(letters, 4))
    return _id


def get_uuid():
    uuid_str = str(uuid.uuid1())
    return uuid_str.replace('-', '')

#课程时间与当前时间比较
def time_status(obj):
    live_channel = LiveChannel.objects.filter(course_id=obj.course_id).first()
    if live_channel:
        stream_status = live_channel.stream_status
    else:
        stream_status = 'test'

    if obj.status == COURSE_REPLAY:
        return COURSE_REPLAY, '录播'
    if not obj.start_time:
        return COURSE_REPLAY, '录播'

    start_time = time.mktime(obj.start_time.timetuple())
    end_time = time.mktime(obj.end_time.timetuple())
    now = time.time()
    #即将直播
    if now < start_time:
        if stream_status == 'normal':
            if obj.status == COURSE_LIVE:
                return COURSE_LIVE, '正在直播'
            else:
                obj.status = COURSE_RESERVATION
                obj.save()
                return COURSE_RESERVATION, '即将直播'
        else:
            return COURSE_RESERVATION, '即将直播'
    #正在直播
    if start_time < now < end_time:
        if obj.status ==COURSE_LIVE:
            if stream_status == 'normal':
                return COURSE_LIVE, '正在直播'
            else:
                return COURSE_LIVE_NOUSER, '正在直播，主播正在赶来的路上'
        else:
            return COURSE_LIVE_NOUSER, '正在直播，主播正在赶来的路上'

    #直播结束
    if now > end_time:
        if obj.status ==COURSE_LIVE:
            if stream_status == 'normal':
                return COURSE_LIVE, '正在直播'
            else:
                obj.status = COURSE_OVER
                obj.save()
                return COURSE_OVER, '直播结束'
        else:
            obj.status = COURSE_OVER
            obj.save()
            return COURSE_OVER, '直播结束'





