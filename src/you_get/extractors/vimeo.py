#!/usr/bin/env python

__all__ = ['vimeo_download', 'vimeo_download_by_id', 'vimeo_download_by_channel', 'vimeo_download_by_channel_id']

from ..common import *
from json import loads
access_token = 'f6785418277b72c7c87d3132c79eec24'  #By Beining

#----------------------------------------------------------------------
def vimeo_download_by_channel(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    """str->None"""
    # https://vimeo.com/channels/464686
    channel_id = match1(url, r'http://vimeo.com/channels/(\w+)')
    vimeo_download_by_channel_id(channel_id, output_dir, merge, info_only)

#----------------------------------------------------------------------
def vimeo_download_by_channel_id(channel_id, output_dir = '.', merge = False, info_only = False):
    """str/int->None"""
    html = get_content('https://api.vimeo.com/channels/{channel_id}/videos?access_token={access_token}'.format(channel_id = channel_id, access_token = access_token))
    data = loads(html)
    id_list = []
    
    #print(data)
    for i in data['data']:
        id_list.append(match1(i['uri'], r'/videos/(\w+)'))
        
    for id in id_list:
        vimeo_download_by_id(id, None, output_dir, merge, info_only)

def vimeo_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    video_page = get_content('http://player.vimeo.com/video/%s' % id, headers=fake_headers)
    title = r1(r'<title>([^<]+)</title>', video_page)
    info = dict(re.findall(r'"([^"]+)":\{[^{]+"url":"([^"]+)"', video_page))
    for quality in ['hd', 'sd', 'mobile']:
        if quality in info:
            url = info[quality]
            break
    assert url
    
    type, ext, size = url_info(url, faker=True)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge, faker = True)

def vimeo_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://vimeo.com/channels/\w+', url):
        vimeo_download_by_channel(url, output_dir, merge, info_only)
    else:
        id = r1(r'http://[\w.]*vimeo.com[/\w]*/(\d+)$', url)
        assert id
    
        vimeo_download_by_id(id, None, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "Vimeo.com"
download = vimeo_download
download_playlist = vimeo_download_by_channel
