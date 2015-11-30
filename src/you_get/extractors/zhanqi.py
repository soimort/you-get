#!/usr/bin/env python

__all__ = ['zhanqi_download']

from ..common import *
import re

def zhanqi_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_content(url)
    video_type_patt = r'VideoType":"([^"]+)"'
    video_type = match1(html, video_type_patt)

    #rtmp_base_patt = r'VideoUrl":"([^"]+)"'
    rtmp_id_patt = r'videoId":"([^"]+)"'
    vod_m3u8_id_patt = r'VideoID":"([^"]+)"'
    title_patt = r'<p class="title-name" title="[^"]+">([^<]+)</p>'
    title_patt_backup = r'<title>([^<]{1,9999})</title>'
    title = match1(html, title_patt) or match1(html, title_patt_backup)
    title = unescape_html(title)
    rtmp_base = "http://wshdl.load.cdn.zhanqi.tv/zqlive"
    vod_base = "http://dlvod.cdn.zhanqi.tv"
    
    if video_type == "LIVE":
        rtmp_id = match1(html, rtmp_id_patt).replace('\\/','/')
        request_url = rtmp_base+'/'+rtmp_id+'.flv?get_url=1'
        real_url = get_html(request_url)
        print_info(site_info, title, 'flv', float('inf'))
        if not info_only:
            #download_rtmp_url(real_url, title, 'flv', {}, output_dir, merge = merge)
            download_urls([real_url], title, 'flv', None, output_dir, merge = merge)
    elif video_type == "VOD":
        vod_m3u8_request = vod_base + match1(html, vod_m3u8_id_patt).replace('\\/','/')
        vod_m3u8 = get_html(vod_m3u8_request)
        part_url = re.findall(r'(/[^#]+)\.ts',vod_m3u8)
        real_url = []
        for i in part_url:
            i = vod_base + i + ".ts"
            real_url.append(i)
        type_ = ''
        size = 0
        for url in real_url:
            _, type_, temp = url_info(url)
            size += temp or 0

        print_info(site_info, title, type_ or 'ts', size)
        if not info_only:
            download_urls(real_url, title, type_ or 'ts', size, output_dir, merge = merge)
    else:
        NotImplementedError('Unknown_video_type')
site_info = "zhanqi.tv"
download = zhanqi_download
download_playlist = playlist_not_supported('zhanqi')
