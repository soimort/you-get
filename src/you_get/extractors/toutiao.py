#!/usr/bin/env python
import binascii
import random
from json import loads
from urllib.parse import urlparse

from ..common import *

try:
    from base64 import decodebytes
except ImportError:
    from base64 import decodestring

    decodebytes = decodestring

__all__ = ['toutiao_download', ]


def random_with_n_digits(n):
    return random.randint(10 ** (n - 1), (10 ** n) - 1)


def sign_video_url(vid):
    r = str(random_with_n_digits(16))

    url = 'https://ib.365yg.com/video/urls/v/1/toutiao/mp4/{vid}'.format(vid=vid)
    n = urlparse(url).path + '?r=' + r
    b_n = bytes(n, encoding="utf-8")
    s = binascii.crc32(b_n)
    aid = 1364
    ts = int(time.time() * 1000)
    return url + '?r={r}&s={s}&aid={aid}&vfrom=xgplayer&callback=axiosJsonpCallback1&_={ts}'.format(r=r, s=s, aid=aid,
                                                                                                    ts=ts)


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
    ret = loads(ret[20:-1])
    vlist = ret.get('data').get('video_list')
    if len(vlist) > 0:
        vInfo = vlist.get(sorted(vlist.keys(), reverse=True)[0])
        vUrl = vInfo.get('main_url')
        vUrl = decodebytes(vUrl.encode('ascii')).decode('ascii')
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
    video_id = match1(html, r".*?videoId: '(?P<vid>.*)'")
    title = match1(html, '.*?<title>(?P<title>.*?)</title>')
    video_file_list = get_file_by_vid(video_id)  # 调api获取视频源文件
    type, ext, size = url_info(video_file_list[0].url, faker=True)
    print_info(site_info=site_info, title=title, type=type, size=size)
    if not info_only:
        download_urls([video_file_list[0].url], title, ext, size, output_dir, merge=merge, faker=True)


site_info = "Toutiao.com"
download = toutiao_download
download_playlist = playlist_not_supported("toutiao")
