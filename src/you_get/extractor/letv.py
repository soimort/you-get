#!/usr/bin/env python

__all__ = ['letv_download']

import json
import xml.etree.ElementTree as ET
from ..common import *

def video_info(vid):
    x = get_content("http://www.letv.com/v_xml/%s.xml" % vid)
    xml_obj = ET.fromstring(x)
    info = json.loads(xml_obj.find("playurl").text)
    title = info.get('title')
    urls = info.get('dispatch')
    for key in urls.keys():
        url = urls[key][0]
        break
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
