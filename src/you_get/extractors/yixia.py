#!/usr/bin/env python

__all__ = ['yixia_download']

from ..common import *
from urllib.parse import urlparse
from json import loads
import re

#----------------------------------------------------------------------
def yixia_miaopai_download_by_scid(scid, output_dir = '.', merge = True, info_only = False):
    """"""
    api_endpoint = 'http://api.miaopai.com/m/v2_channel.json?fillType=259&scid={scid}&vend=miaopai'.format(scid = scid)
    
    html = get_content(api_endpoint)
    
    api_content = loads(html)
    
    video_url = match1(api_content['result']['stream']['base'], r'(.+)\?vend')
    title = api_content['result']['ext']['t']
    
    type, ext, size = url_info(video_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, output_dir, merge=merge)

#----------------------------------------------------------------------
def yixia_xiaokaxiu_download_by_scid(scid, output_dir = '.', merge = True, info_only = False):
    """"""
    api_endpoint = 'http://api.xiaokaxiu.com/video/web/get_play_video?scid={scid}'.format(scid = scid)
    
    html = get_content(api_endpoint)
    
    api_content = loads(html)
    
    video_url = api_content['data']['linkurl']
    title = api_content['data']['title']
    
    type, ext, size = url_info(video_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, output_dir, merge=merge)

#----------------------------------------------------------------------
def yixia_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    """wrapper"""
    hostname = urlparse(url).hostname
    if 'miaopai.com' in hostname:  #Miaopai
        yixia_download_by_scid = yixia_miaopai_download_by_scid
        site_info = "Yixia Miaopai"
        
        if re.match(r'http://www.miaopai.com/show/channel/\w+', url):  #PC
            scid = match1(url, r'http://www.miaopai.com/show/channel/(\w+)')
        elif re.match(r'http://www.miaopai.com/show/\w+', url):  #PC
            scid = match1(url, r'http://www.miaopai.com/show/(\w+)')
        elif re.match(r'http://m.miaopai.com/show/channel/\w+', url):  #Mobile
            scid = match1(url, r'http://m.miaopai.com/show/channel/(\w+)')
    
    elif 'xiaokaxiu.com' in hostname:  #Xiaokaxiu
        yixia_download_by_scid = yixia_xiaokaxiu_download_by_scid
        site_info = "Yixia Xiaokaxiu"
        
        if re.match(r'http://v.xiaokaxiu.com/v/.+\.html', url):  #PC
            scid = match1(url, r'http://v.xiaokaxiu.com/v/(.+)\.html')
        elif re.match(r'http://m.xiaokaxiu.com/m/.+\.html', url):  #Mobile
            scid = match1(url, r'http://m.xiaokaxiu.com/m/(.+)\.html')

    else:
        pass
    
    yixia_download_by_scid(scid, output_dir, merge, info_only)

site_info = "Yixia"
download = yixia_download
download_playlist = playlist_not_supported('yixia')

#Another way
#----------------------------------------------------------------------
#def yixia_miaopai_download_by_scid(scid, output_dir = '.', merge = True, info_only = False):
    #""""""
    #headers = {
    #'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
    #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Cache-Control': 'max-age=0',
    #}

    #html = get_content('http://m.miaopai.com/show/channel/' + scid, headers)

    #title = match1(html, r'<title>(\w+)')

    #video_url = match1(html, r'<div class="vid_img" data-url=\'(.+)\'')

    #type, ext, size = url_info(video_url)

    #print_info(site_info, title, type, size)
    #if not info_only:
        #download_urls([video_url], title, ext, size, output_dir, merge=merge)
