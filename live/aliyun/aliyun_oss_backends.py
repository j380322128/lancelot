# coding: utf-8
from django.conf import settings

from aliyun_oss2_storage.backends import AliyunBaseStorage


class AliyunCDNBaseStorage(AliyunBaseStorage):
    def url(self, name):
        name = self._normalize_name(self._clean_name(name))

        cdn_url = settings.ALIYUN_OSS_CDN_URL + name
        return cdn_url

    def _save(self, name, content):
        # 区分静态文件，上传文件
        if name.startswith("uploads"):
            target_name = "".join([settings.ALIYUN_OSS_DIRECTORY_PREFIX, name])
        else:
            target_name = "".join([settings.STATIC_URL[1:], name])

        content.open()
        content_str = b''.join(chunk for chunk in content.chunks())
        self.bucket.put_object(target_name, content_str)
        content.close()

        return self._clean_name(name)


class AliyunCDNMediaStorage(AliyunCDNBaseStorage):
    location = settings.MEDIA_URL


class AliyunCDNStaticStorage(AliyunCDNBaseStorage):
    location = settings.STATIC_URL