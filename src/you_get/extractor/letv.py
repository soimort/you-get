#!/usr/bin/env python

__all__ = ['letv_download']

import json
import random
import xml.etree.ElementTree as ET
from ..common import *

def get_timestamp():
    tn = random.random()
    url = 'http://api.letv.com/time?tn={}'.format(tn)
    result = get_content(url)
    return json.loads(result)['stime']

def get_key(t):
    for s in range(0, 8):
        e = 1 & t
        t >>= 1
        e <<= 31
        t += e
    return t ^ 185025305

def video_info(vid):
    tn = get_timestamp()
    key = get_key(tn)
    url = 'http://api.letv.com/mms/out/video/play?id={}&platid=1&splatid=101&format=1&tkey={}&domain=http%3A%2F%2Fwww.letv.com'.format(vid, key)
    r = get_content(url, decoded=False)
    xml_obj = ET.fromstring(r)
    info = json.loads(xml_obj.find("playurl").text)
    title = info.get('title')
    urls = info.get('dispatch')
    for k in urls.keys():
        url = urls[k][0]
        break
    url += '&termid=1&format=0&hwtype=un&ostype=Windows7&tag=letv&sign=letv&expect=1&pay=0&rateid={}'.format(k)
    return url, title

def letv_download_by_vid(vid, output_dir='.', merge=True, info_only=False):
    url, title = video_info(vid)
    _, _, size = url_info(url)
    ext = 'flv'
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def letv_download(url, output_dir='.', merge=True, info_only=False):
    if re.match(r'http://www.letv.com/ptv/vplay/(\d+).html', url):
        vid = match1(url, r'http://www.letv.com/ptv/vplay/(\d+).html')
    else:
        html = get_content(url)
        vid = match1(html, r'vid="(\d+)"')
    letv_download_by_vid(vid, output_dir=output_dir, merge=merge, info_only=info_only)


site_info = "letv.com"
download = letv_download
download_playlist = playlist_not_supported('letv')
