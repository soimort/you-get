#!/usr/bin/env python
__all__ = ['iwara_download']
from ..common import *
from ..common import print_more_compatible as print
from ..extractor import VideoExtractor
from ..util import log
from .. import json_output
headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.dilidili.com/',
    'Connection': 'keep-alive',
    'Save-Data': 'on',
}



def iwara_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    global headers
    video_hash=match1(url, r'http://ecchi.iwara.tv/videos/(\w+)')
    html = get_html(url)
    title = r1(r'<title>(.*)</title>', html)
    api_url='http://ecchi.iwara.tv/api/video/'+video_hash
    content=get_html(api_url)
    mime='video/mp4'
    size=0;
    print_info(content,title,mime,size)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([source], title, ext, size, output_dir, merge=merge)

site_info = "iwara"
download = iwara_download
download_playlist = playlist_not_supported('archive')