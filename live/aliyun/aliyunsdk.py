# coding: utf-8

"""
aliyun SDK
"""
from django.conf import settings
from .aliyun_request import AliyunRequestCDN
from .utils import (
    nowtime,
    utc_nowtime,
    timestamp2utc,
    timestamp2utc_string,
    datetimestr2utcstr,
)

import logging
logger = logging.getLogger('aliyun')

# 推流
ALIYUN_LIVE_PUSH_URL_TEMPLATE = "rtmp://{domain}/{app_name}/{stream_name}?vhost={cdn_domain}"
# 拉流
ALIYUN_LIVE_PULL_TEMPLATE_RTMP = "rtmp://{cdn_domain}/{app_name}/{stream_name}"
ALIYUN_LIVE_PULL_TEMPLATE_FLV = "http://{cdn_domain}/{app_name}/{stream_name}.flv"
ALIYUN_LIVE_PULL_TEMPLATE_HLS = "http://{cdn_domain}/{app_name}/{stream_name}.m3u8"



class Client(object):
    def __init__(self, api_domain, version):
        self.version = version
        self.api_domain = api_domain

    def get_domain_request(self, action, cdn_domain=None):
        request = AliyunRequestCDN(self.version)
        querystring = {
            "Action": "DescribeLiveStreamsBlockList",
        }
        if cdn_domain:
            querystring["DomainName"] = cdn_domain
        return request, querystring

    def get_stream_request(self, action, cdn_domain=None, app_name=None, stream_name=None):
        request = AliyunRequestCDN(self.version)
        querystring = {
            "Action": action
        }

        if cdn_domain:
            querystring["DomainName"] = cdn_domain
        if app_name:
            querystring["AppName"] = app_name
        if stream_name:
            querystring["StreamName"] = stream_name

        return request, querystring


class AliyunLiveClient(Client):
    def __init__(self):
        Client.__init__(self, settings.ALIYUN_API_DOMAIN_LIVE, "2016-11-01")

    def set_authentication(self):
        """
        根据鉴权key获得加密之后的拉流或者推流地址
        """

    def create_channel(self, enterprise):
        """
        @params: enterprise 企业英文名 改为企业号外加课程号
        @params: enterprise 企业英文名 改为企业号外加课程号
        @return:
            {"pulish_url": "", "pull_hls": "", "pull_flv": "", "pull_rtmp": ""}
        """
        # TODO: 判断那个域名下的正在推流是否达到限制，
        # 鉴权
        cdn_domain = settings.ALIYUN_LIVE_CDN_DOMAIN

        # stream name: timestamp + enterprise
        strean_name = nowtime() + enterprise
        # 拼接自定义推流地址
        pulish_format_data = {
            "domain": settings.ALIYUN_LIVE_PUSH_DOMAIN,
            "app_name": enterprise,
            "stream_name": strean_name,
            "cdn_domain": cdn_domain,
        }
        pulish_rtmp = ALIYUN_LIVE_PUSH_URL_TEMPLATE.format(**pulish_format_data)

        # 拼接拉流地址
        pull_format_data = {
            "cdn_domain": cdn_domain,
            "app_name": enterprise,
            "stream_name": strean_name
        }
        # rtmp 拉流
        pull_rtmp = ALIYUN_LIVE_PULL_TEMPLATE_RTMP.format(**pull_format_data)
        # flv 拉流
        pull_flv = ALIYUN_LIVE_PULL_TEMPLATE_FLV.format(**pull_format_data)
        # hls(m3u8) 拉流
        pull_hls = ALIYUN_LIVE_PULL_TEMPLATE_HLS.format(**pull_format_data)

        # return data
        data = {
            "pulish_url": pulish_rtmp,
            "pull_hls": pull_hls,
            "pull_flv": pull_flv,
            "pull_rtmp": pull_rtmp
        }
        return data

    def set_live_streams_notify_url_config(self, cdn_domain, notify_url):
        """
        设置直播流信息推送到的URL地址。
        @params: cdn_domain 推流加速域名
        @params: notify_url 设置直播流信息推送到的URL地址，必须以http://开头；
        """
        action = "SetLiveStreamsNotifyUrlConfig"

        request, querystring = self.get_stream_request(action, cdn_domain)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def get_live_streams_online_list(self, cdn_domain, app_name=None):
        """
        查看指定域名下（或者指定域名下某个应用）的所有正在推的流的信息
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @return:
            {
                "RequestId": "0D70427D-91E4-4349-AAD3-5511A5BB823B", 
                "OnlineInfo": {
                    "LiveStreamOnlineInfo": [
                        {
                            "AppName": "xchen", 
                            "StreamName": "testxchen", 
                            "PublishTime": "2015-12-02T06:58:04Z", 
                            "PublishUrl": "rtmp://cdntrans.w.alikunlun.com:1935/xchen", 
                            "DomainName": "test101.aliyunlive.com"
                        }
                    ]
                }
            }
        """
        action = "DescribeLiveStreamsOnlineList"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name=app_name)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def forbidden_or_resume_pulish_stream(self, cdn_domain, app_name, stream_name, forbi_resume="forbidden"):
        """
        禁止/恢复推流
        rtmp://center_domain/app_name/stream_name/
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @params: forbi_resume 禁止(forbidden)/恢复(resume)
        """
        action_dict = {
            "forbidden": "ForbidLiveStream",
            "resume": "ResumeLiveStream"
        }
        action = action_dict.get(forbi_resume)
        if not action:
            raise

        request, querystring = self.get_stream_request(action, cdn_domain, app_name, stream_name)
        querystring["AppName"] = app_name
        querystring["StreamName"] = stream_name
        querystring["LiveStreamType"] = "publisher"

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def get_live_stream_online_user_num(self, cdn_domain, app_name, stream_name, start_time=None, end_time=None):
        """
        查询在线人数
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @params: start_time 开始时间戳
        @params: end_time 结束时间戳
        @return:
            {
                "OnlineUserInfo": {
                    "LiveStreamOnlineUserNumInfo": [
                        {
                            "StreamUrl": "rtmp://test101.cdnpe.com/live/test101", 
                            "UserNumber": 2
                        }, 
                        {
                            "StreamUrl": "rtmp://test101.cdnpe.com/live/test102", 
                            "UserNumber": 5
                        }
                    ]
                }, 
                "TotalUserNumber": 7
            }
        """
        action = "DescribeLiveStreamOnlineUserNum"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name, stream_name)
        if start_time and end_time:
            querystring["StartTime"] = timestamp2utc_string(start_time)
            querystring["EndTime"] = timestamp2utc_string(end_time)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def get_live_streams_publish_list(self, cdn_domain, start_time, end_time, app_name=None, stream_name=None):
        """
        查询某个时间段推流历史, 二级，三级没传直接cdn下面所有的流
        @params: cdn_domain 推流加速域名
        @params: start_time 开始时间戳
        @params: end_time 结束时间戳
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @return:
            {
                "OnlineUserInfo": {
                    "LiveStreamOnlineUserNumInfo": [
                        {
                            "StreamUrl": "rtmp://test101.cdnpe.com/live/test101", 
                            "UserNumber": 2
                        }, 
                        {
                            "StreamUrl": "rtmp://test101.cdnpe.com/live/test102", 
                            "UserNumber": 5
                        }
                    ]
                }, 
                "TotalUserNumber": 7
            }
        """
        action = "DescribeLiveStreamsPublishList"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name, stream_name)
        querystring["StartTime"] = timestamp2utc_string(start_time)
        querystring["EndTime"] = timestamp2utc_string(end_time)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def get_live_stream_record_content(self, cdn_domain, app_name, stream_name, start_time, end_time):
        """
        查询某路直播流录制内容。
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @params: start_time 开始时间戳
        @params: end_time 结束时间戳
        @return:
            {}
        """
        action = "DescribeLiveStreamRecordContent"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name, stream_name)
        querystring["StartTime"] = timestamp2utc_string(start_time)
        querystring["EndTime"] = timestamp2utc_string(end_time)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def get_live_stream_record_index_files(self, cdn_domain, app_name, stream_name, start_time, end_time):
        """
        得到某个时间段下appname下的某个streamname。录制文件路径
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @params: start_time 开始时间戳
        @params: end_time 结束时间戳
        @return:
            {
              "RecordIndexInfoList": {
                "RecordIndexInfo": [
                  {
                    "OssBucket": "bucket",
                    "OssEndpoint": "oss-cn-hangzhou.aliyuncs.com",
                    "OssObject": "atestObject.m3u8",
                    "RecordId": "c4d7f0a4-b506-43f9-8de3-07732c3f3d82",
                    "DomainName": "xxx",
                    "AppName": "xxx",
                    "StreamName": "xxx",
                    "Duration": 588.849,
                    "Height": 480,
                    "Width": 640,
                    "StartTime": "2016-05-25T05:37:11Z",
                    "EndTime": "2016-05-25T05:47:11Z",
                    "CreateTime": "2016-05-27T09:40:56Z",
                    "RecordUrl": "http://xxx.xxx/atestObject.m3u8"
                  }
                ]
              },
              "RequestId": "DE24625C-7C0F-4020-8448-9C31A50C1556"
            }
        """
        action = "DescribeLiveStreamRecordIndexFiles"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name, stream_name)
        querystring["StartTime"] = start_time
        querystring["EndTime"] = end_time

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def add_live_app_record_config(self, cdn_domain, app_name, oss_bucket, prefix, record_format='m3u8'):
        """
        配置APP录制，输出内容保存到OSS中
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: oss_bucket oss存储bucket名称
        @params: prefix oss存储的录制文件名前缀
        @return :
        {
            "RequestId": "16A96B9A-F203-4EC5-8E43-CB92E68F4CD8", 
        }
        """
        action = "AddLiveAppRecordConfig"
        request, querystring = self.get_stream_request(action, cdn_domain, app_name)
        querystring['OssEndpoint'] = settings.ALIYUN_OSS_ENDPOINT
        querystring['OssBucket'] = oss_bucket
        querystring['RecordFormat.1.Format'] = record_format
        querystring['RecordFormat.1.OssObjectPrefix'] = prefix + "/{AppName}/{StreamName}_{Sequence}_{StartTime}_{EndTime}"
        querystring[
            'RecordFormat.1.SliceOssObjectPrefix'] = prefix + "/{Date}/{AppName}/{StreamName}/{UnixTimestamp}_{Sequence}"

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def delete_live_app_record_config(self, cdn_domain, app_name):
        """
        解除录制配置
        @params: cdn_domain 推流加速域名
        @params: app_name 创建推流时候二级
        @params: stream_name 三级
        @return :
        {
            "RequestId": "16A96B9A-F203-4EC5-8E43-CB92E68F4CD8", 
        }
        """
        action = "DeleteLiveAppRecordConfig"

        request, querystring = self.get_stream_request(action, cdn_domain, app_name)

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def add_live_record_notify_config(self, cdn_domain, notify_url, need_status_notify='false'):
        """
        添加域名级别录制回调配置，以下状态下会通知
        1.表示目标录制文件已经生成
        2.录制开始件回调, 表示录制已经成功开始
        3.录制暂停事件回调, 表示录制已经成功暂停事
        4.录制继续事件回调, 表示录制已经成功恢复
        @params: cdn_domain 推流加速域名
        @params: notify_url 回掉地址
        @params: need_notify_status 是否需要回掉(false/true)
        1:阿里云访问请求数据:
            {
              "domain": "qt01.alivecdn.com",
              "app": "mp4flvtest_flv",
              "stream": "callback_test",
              "uri": "mp4flvtest_flv/callback_test/0_2017-03-08-23:09:46_2017-03-08-23:10:40.flv",
              "duration": 69.403,
              "start_time": 1488985786,
              "stop_time": 1488985840
            }
        2,3,4:@阿里云访问请求数据:
            {
              "domain": "gs_domain",
              "app": "gs_app",
              "stream": "gs_stream",
              "event": "record_started"
            }
        """
        action = "AddLiveRecordNotifyConfig"

        request, querystring = self.get_stream_request(action, cdn_domain)
        querystring['NotifyUrl'] = notify_url
        querystring['NeedStatusNotify'] = need_status_notify
        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def update_live_record_notify_config(self, cdn_domain, notify_url, need_status_notify='false'):
        """
        更新域名级别录制回调配置，以下状态下会通知

        """
        action = "UpdateLiveRecordNotifyConfig"

        request, querystring = self.get_stream_request(action, cdn_domain)
        querystring['NotifyUrl'] = notify_url
        querystring['NeedStatusNotify'] = need_status_notify
        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def live_stream_transcode(self, cdn_domain, app_name, template="lld,lsd,lud", operating="add"):
        """
        添加或删除转码配置
        @params: operating add | delete
        """
        action = "AddLiveStreamTranscode" if operating == "add" else "DeleteLiveStreamTranscode"

        request, querystring = self.get_stream_request(action)
        querystring['Domain'] = cdn_domain
        querystring['App'] = app_name
        querystring['Template'] = template
        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def describe_live_stream_transcode_info(self, cdn_domain):
        """
        查询转码配置
        """
        action = "DescribeLiveStreamTranscodeInfo"

        request, querystring = self.get_stream_request(action)
        querystring['DomainTranscodeName'] = cdn_domain
        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def test(self):
        request = AliyunRequestCDN()
        querystring = {
            "Action": "DescribeLiveStreamsBlockList",
            "DomainName": "video.ullget.cn",
        }
        response = request.request("GET", self.api_domain, params=querystring)


class AliyunVodClient(Client):
    """
    点播
    """

    def __init__(self):
        Client.__init__(self, settings.ALIYUN_API_DOMAIN_VOD)

    def add_media(self, file_url):
        pass


class MTSClient(Client):
    """
    媒体转码
    """

    def __init__(self):
        Client.__init__(self, settings.ALIYUN_API_DOMAIN_MTS, "2014-06-18")

    def add_water_mark_template(self, name, config=None):
        """
        新增水印模板
        @params: name 模板名
        @params: config: {
            "Width": "10",
            "Height": "30",
            "Dx": "10",
            "Dy": "5",
            "ReferPos": "TopRight",
            "Type": "Image"
        }
        @return:
             {
              "RequestId": "25818875-5F78-4A13-BEF6-D7393642CA58",
              "WaterMarkTemplate": {
                    "Id": "88c6ca184c0e47098a5b665e2a126797",
                    "Name": "example-watermark",
                    "Width": "10",
                    "Height": "30",
                    "Dx": "10",
                    "Dy": "5",
                    "ReferPos": "TopRight",
                    "Type": "Image",
                    "State": "Normal"
                }
            }
        """
        action = ""

        _config = {
            "Width": "10",
            "Height": "30",
            "Dx": "10",
            "Dy": "5",
            "ReferPos": "TopRight",
            "Type": "Image"
        }

        if config:
            _config.update(config)

        request, querystring = self.get_stream_request(action)
        querystring['Name'] = name
        querystring['Config'] = _config

        response = request.request("GET", self.api_domain, params=querystring)
        return response

    def SearchWaterMarkTemplate(self, page_number, page_size, state):
        """
        搜索指定状态的水印模板。
        @params: page_number 页码
        @params: page_size 每页条数
        @params: state 水印模板状态：All表示所有，Normal表示正常，Deleted表示已删除的，默认是All。
        @return: 
             {
                 "RequestId": "25818875-5F78-4A13-BEF6-D7393642CA58",
                    "TotalCount": 100,
                    "PageNumber": 1,
                    "PageSize": 10,
                    "WaterMarkTemplateList": {
                        "WaterMarkTemplate": [{
                            "Id": "88c6ca184c0e47098a5b665e2a126797",
                            "Name": "example-watermark",
                            "Width": "10",
                            "Height": "30",
                            "Dx": "10",
                            "Dy": "5",
                            "ReferPos": "TopRight",
                            "Type": "Image",
                            "State": "Normal"
                            }]
                    }
                }
        """
        action = "SearchWaterMarkTemplate"

        request, querystring = self.get_stream_request(action)
        querystring['PageNumber'] = page_number
        querystring['PageSize'] = page_size
        querystring['State'] = state

        response = request.request("GET", self.api_domain, params=querystring)
        return response


def main():
    client = AliyunLiveClient()
    # response = client.get_live_stream_online_user_num("video.ullget.cn", "test", "test") datetimestr2utcstr
    start_time = datetimestr2utcstr("2017-03-19 11:28:37")
    end_time = datetimestr2utcstr("2017-03-21 11:33:29")

    response = client.get_live_stream_record_index_files("live.ullget.cn", "record", "record1", start_time, end_time)
    logger.info(response)


if __name__ == "__main__": main()
