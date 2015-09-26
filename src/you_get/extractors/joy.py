#!/usr/bin/env python

__all__ = ['joy_download']

from ..common import *

def video_info(channel_id, program_id, volumn_id):
    url = 'http://msx.app.joy.cn/service.php'
    if program_id:
        url += '?action=vodmsxv6'
        url += '&channelid=%s' % channel_id
        url += '&programid=%s' % program_id
        url += '&volumnid=%s' % volumn_id
    else:
        url += '?action=msxv6'
        url += '&videoid=%s' % volumn_id
    
    xml = get_html(url)
    
    name = r1(r'<Title>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</Title>', xml)
    urls = re.findall(r'<Url[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</Url>', xml)
    hostpath = r1(r'<HostPath[^>]*>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</HostPath>', xml)
    
    return name, urls, hostpath

def joy_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    channel_id = r1(r'[^_]channelId\s*:\s*"([^\"]+)"', get_html(url))
    program_id = r1(r'[^_]programId\s*:\s*"([^\"]+)"', get_html(url))
    volumn_id = r1(r'[^_]videoId\s*:\s*"([^\"]+)"', get_html(url))
    
    title, urls, hostpath = video_info(channel_id, program_id, volumn_id)
    urls = [hostpath + url for url in urls]
    
    size = 0
    for url in urls:
        _, ext, temp = url_info(url)
        size += temp
    
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir = output_dir, merge = merge)

site_info = "Joy.cn"
download = joy_download
download_playlist = playlist_not_supported('joy')
