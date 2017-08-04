# -*- coding: utf-8 -*-
'''
信信客短信获取
'''
import requests
import hashlib
import random
import logging
import json

from django.core.cache import cache

from django.conf import settings


logger = logging.getLogger('sdk')


class VerificationCode(object):
    '''
    验证码
    '''
    # 全局存放 手机号跟验证码
    data = {}

    @classmethod
    def save(cls, phone, code):
        '''
        使用 cache 保存phone, code
        :param phone:
        :param code:
        :return:
        '''
        logger.info("VerificationCode ----  set %s' code: %s" % (phone, code))
        # cls.data[phone] = code
        cache.set(phone, code)

    @classmethod
    def get_code_by_phone(cls, phone):
        # code = cls.data.get(phone, None)
        code = cache.get(phone)
        logger.info("VerificationCode ----  get %s' code: %s" % (phone, code))
        return code

    @classmethod
    def _generate_verification_code(cls, length=6):
        '''
        生成验证码
        :param length: 验证码长度
        :return:
        '''
        code_list = []
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        # for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        #     code_list.append(chr(i))
        # for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        #     code_list.append(chr(i))
        my_slice = random.sample(code_list, length)  # 从list中随机获取6个元素，作为一个片断返回
        verification_code = ''.join(my_slice)
        return verification_code

    @classmethod
    def send_verification_code(cls, phone):
        '''
        根据手机号码发送验证码
        :param phone:
        :return: '{"data":{"message":"提交成功","mobiles":[{"index":"149086321497986802","mobile":"13627282126"}]},"code":"25010"}'
        '''
        md = hashlib.md5()
        md.update((settings.XXK_DEV_ID + settings.XXK_DEV_KEY + phone).encode('utf8'))
        sign = md.hexdigest()
        number = cls._generate_verification_code(6)
        payload = {
            'dev_id': settings.XXK_DEV_ID,
            'sign': sign,
            'sms_template_code': '88888888',
            'rec_num': phone,
            'sms_param': "{\"code\":\"" + number + "\"}"
        }
        res = requests.post(settings.XXK_URL, data=payload)
        return res, number

    @classmethod
    def send_course_notify_message(cls, phone, course_title, teacher_name, start_time):
        """
        发送提醒信息
        """
        sign = cls.sign(phone)
        param = {
            "title": course_title,
            "teacher_name": teacher_name,
            "start_time": start_time
        }
        payload = {
            'dev_id': settings.XXK_DEV_ID,
            'sign': sign,
            'sms_template_code': 'course_notify',
            'rec_num': phone,
            'sms_param': json.dumps(param)
        }
        res = requests.post(settings.XXK_URL, data=payload)
        return res

    @classmethod
    def sign(cls, phone):
        md = hashlib.md5()
        md.update((settings.XXK_DEV_ID + settings.XXK_DEV_KEY + phone).encode('utf8'))
        sign = md.hexdigest()
        return sign
