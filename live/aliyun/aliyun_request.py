# coding: utf-8
import requests
import logging
import base64
import json
import rsa
import os

from urllib import urlencode

from django.conf import settings
from requests.compat import json as _json

from .utils import (
        utc_nowtime,
        nowtime,
        get_signature_string,
        aliyun_sgin,
        datetime2string
    )

logger = logging.getLogger('aliyun')

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PEM_PATH = "".join([BASE_PATH, "/pem/"+settings.PROJECT_NAME+"/app_private_key.pem"])


class ClientException(Exception):
    pass


class Request(object):
    def get_check(self, json):
        """
        检测微信公众平台返回值中是否包含错误的返回码。
        如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
        """
        if "Code" in json:
            raise ClientException("{}: {}".format(json["Code"], json["Message"]))
        return json

    def request(self, method, url, **kwargs):
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            verify=False,
            **kwargs
        )
        r.raise_for_status()
        json = r.json()
        return self.get_check(json)

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )


class AliyunRequestCDN(Request):
    def __init__(self, version):
        self.version = version

    def request(self, method, url, **kwargs):
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        params = kwargs.get("params")
        if not params:
            params = {}
        # 公共参数
        params["Format"] = "JSON"
        params["Version"] = self.version
        params["AccessKeyId"] = settings.ALIYUN_ACCESS_KEY
        params["SignatureMethod"] = "HMAC-SHA1"
        params["Timestamp"] = utc_nowtime()
        params["SignatureVersion"] = "1.0"
        params["SignatureNonce"] = nowtime()

        # 代签名字符串
        sign_string = get_signature_string(params)
        # 签名字符串
        signature = aliyun_sgin(settings.ALIYUN_SECRET, sign_string)
        params["Signature"] = signature

        kwargs['params'] = params

        r = requests.request(
            method=method,
            url=url,
            verify=False,
            **kwargs
        )
        
        json = r.json()
        return self.get_check(json)


class AliPayClient(object):
    def __init__(self, appid, partner_id):
        self.appid = appid
        self.partner_id = partner_id

    def signature(self, string):
        """
        签名(RSAwithSHA1),使用openssl 生成app_privete_key.pem
        """
        # 读取pem private key文件
        logger.info('PEM_PATH: {}'.format(PEM_PATH))
        with open(PEM_PATH, 'rb') as privatekey_file:
            pub = privatekey_file.read()
        # 加密
        privatekey = rsa.PrivateKey.load_pkcs1(pub)
        signature = rsa.sign(string.encode("utf-8"), privatekey, "SHA-1")
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        return signature_base64

    def aliverify(self, response_data):
        """
        
        """

    def trade_precreate(self, precreate_data):
        """
        二维码支付
        """
        _data = {
            "app_id": self.appid,
            "method": "alipay.trade.precreate",
            "format": "JSON",
            "charset": "UTF-8",
            "sign_type": "RSA",
            "timestamp": datetime2string(),
            "version": "1.0",
            "notify_url": "http://www.ullget.com/alipay/notify"
        }
        _data['biz_content'] = json.dumps(precreate_data)

        logger.info("trade precreate data: {}".format(_data))

        res = self.__async_request(_data)
        return res

    def trade_wap(self, wap_data, return_url=None):
        """
        WAP支付
        """
        _data = {
            "app_id": self.appid,
            "method": "alipay.trade.wap.pay",
            "format": "JSON",
            "charset": "UTF-8",
            "sign_type": "RSA",
            "timestamp": datetime2string(),
            "version": "1.0",
        }
        if return_url:
            _data['return_url'] = return_url
        _data['biz_content'] = json.dumps(wap_data).replace(" ", "")

        logger.info("trade wap data: {}".format(_data))

        params = list(_data.items())

        logger.info("params: {}".format(params))

        params.sort()
        string = "&".join(["%s=%s" % (str(p[0]), str(p[1])) for p in params])
        # 加入签名
        sign = self.signature(string)
        logger.info("sign:{}".format(sign))
        # urlencode
        params.append(("sign", sign))
        string = "&".join(["%s=%s" % (str(p[0]), urlencode({"key": str(p[1])}).split("=", 1)[1]) for p in params])
        wap_url = "".join([settings.ALIPAY_GATEWAY, "?", string])

        logger.info("wap_url :{}".format(wap_url))
        return wap_url

    def order_query(self, out_trade_no):
        """
        订单查询
        """
        _data = {
            "app_id": self.appid,
            "method": "alipay.trade.query",
            "format": "JSON",
            "charset": "UTF-8",
            "sign_type": "RSA",
            "timestamp": datetime2string(),
            "version": "1.0",
        }
        _data['biz_content'] = json.dumps({
            "out_trade_no": out_trade_no
        }, ensure_ascii=False)

        logger.info("order query data: {}".format(_data))

        res = self.__async_request(_data)
        return res

    def __async_request(self, data):
        # 参与签名字段排序,拼接
        params = list(data.items())

        logger.info("params: {}".format(params))

        params.sort()
        string = "&".join(["%s=%s" % (str(p[0]), str(p[1])) for p in params])
        # 加入签名
        sign = self.signature(string)
        logger.info("sign:{}".format(sign))
        data.update({
                "sign": str(sign)
            })

        response = requests.post(settings.ALIPAY_GATEWAY, data=data)
        logger.info("response body: {}, {}".format(response.content, response.text))

        body = response.json()
        return body

try:
    alipay_client
except NameError:
    alipay_client = AliPayClient(settings.ALIPAY_APPID, settings.ALIPAY_PARTNER_ID)
