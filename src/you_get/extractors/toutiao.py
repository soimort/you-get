#!/usr/bin/env python
import base64

from ..common import *
import random
from json import loads

__all__ = ['toutiao_download', ]


# magic function
def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

import ctypes


def unsigned_right_shitf(n, i):
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def gen_table():
    t = [0] * 256
    for r in range(256):
        e = r
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        e = (-306674912 ^ unsigned_right_shitf(e, 1)
             ) if 1 & e else unsigned_right_shitf(e, 1)
        t[r] = e
    return t

table = gen_table()


def sign_url(r, url):
    a = len(url)
    t = -1
    n = -1
    o = -1
    for i in range(a):
        t = ord(url[i])
        if t < 128:
            o = unsigned_right_shitf(o, 8) ^ r[255 & (o ^ t)]
    return o ^ -1


def sign_video_url(vid):
    href = "http://i.snssdk.com/video/urls/v/1/toutiao/mp4/" + vid
    o = "/video/urls/v/1/toutiao/mp4/" + vid + "?r=" + \
        str(random.randint(10000000000000000, 999999999999999999))
    t = sign_url(table, o)
    i = 4294967296 + t if t < 0 else t
    return "http:" + "//" + "i.snssdk.com" + o + "&s=" + str(i)


class ToutiaoVideoInfo(object):

    def __init__(self):
        self.bitrate = None
        self.definition = None
        self.size = None
        self.height = None
        self.width = None
        self.type = None
        self.url = None

    def __str__(self):
        return json.dumps(self.__dict__)


def get_file_by_vid(video_id):
    vRet = []
    url = sign_video_url(video_id)
    ret = get_content(url)
    ret = loads(ret)
    vlist = ret.get('data').get('video_list')
    if len(vlist) > 0:
        vInfo = vlist.get(sorted(vlist.keys(), reverse=True)[0])
        vUrl = vInfo.get('main_url')
        vUrl = base64.decodestring(vUrl.encode('ascii')).decode('ascii')
        videoInfo = ToutiaoVideoInfo()
        videoInfo.bitrate = vInfo.get('bitrate')
        videoInfo.definition = vInfo.get('definition')
        videoInfo.size = vInfo.get('size')
        videoInfo.height = vInfo.get('vheight')
        videoInfo.width = vInfo.get('vwidth')
        videoInfo.type = vInfo.get('vtype')
        videoInfo.url = vUrl
        vRet.append(videoInfo)
    return vRet


def toutiao_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url, faker=True)
    video_id = match1(html, r"videoid\s*:\s*'([^']+)',\n")
    title = match1(html, r"title: '([^']+)'.replace")
    video_file_list = get_file_by_vid(video_id)  # 调api获取视频源文件
    type, ext, size = url_info(video_file_list[0].url, faker=True)
    log.d(video_file_list[0].url)
    print_info(site_info=site_info, title=title, type=type, size=size)
    if not info_only:
        download_urls(
            [video_file_list[0].url],
            title,
            ext,
            size,
            output_dir,
            merge=merge,
            faker=True)


site_info = "Toutiao.com"
download = toutiao_download
download_playlist = playlist_not_supported("toutiao")
