#!/usr/bin/env python

__all__ = ['yixia_miaopai_download']

from ..common import *

#----------------------------------------------------------------------
def yixia_miaopai_download_by_scid(scid, output_dir = '.', merge = True, info_only = False):
    """"""
    headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    }

    html = get_content('http://m.miaopai.com/show/channel/' + scid, headers)

    title = match1(html, r'<title>(\w+)')

    video_url = match1(html, r'<div class="vid_img" data-url=\'(.+)\'')

    type, ext, size = url_info(video_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, output_dir, merge=merge)

#----------------------------------------------------------------------
def yixia_miaopai_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    """wrapper"""
    if re.match(r'http://www.miaopai.com/show/channel/\w+', url):
        scid = match1(url, r'http://www.miaopai.com/show/channel/(\w+)')
    elif re.match(r'http://www.miaopai.com/show/\w+', url):
        scid = match1(url, r'http://www.miaopai.com/show/(\w+)')
    elif re.match(r'http://m.miaopai.com/show/channel/\w+', url):
        scid = match1(url, r'http://m.miaopai.com/show/channel/(\w+)')
    else:
        pass
    yixia_miaopai_download_by_scid(scid, output_dir, merge, info_only)

site_info = "Yixia MiaoPai"
download = yixia_miaopai_download
download_playlist = playlist_not_supported('yixia_miaopai')
