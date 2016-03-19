#!/usr/bin/env python

__all__ = ['zhanqi_download']

from ..common import *
import re
import base64
import json
import time
import hashlib

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
    rtmp_real_base = "rtmp://dlrtmp.cdn.zhanqi.tv/zqlive/"
    room_info = "http://www.zhanqi.tv/api/static/live.roomid/"
    KEY_MASK = "#{&..?!("
    ak2_pattern = r'ak2":"\d-([^|]+)'
    
    if video_type == "LIVE":
        rtmp_id = match1(html, rtmp_id_patt).replace('\\/','/')
        #request_url = rtmp_base+'/'+rtmp_id+'.flv?get_url=1'
        #real_url = get_html(request_url)
        html2 = get_content(room_info + rtmp_id.split("_")[0] + ".json")
        json_data = json.loads(html2)
        cdns = json_data["data"]["flashvars"]["cdns"]
        cdns = base64.b64decode(cdns).decode("utf-8")
        cdn = match1(cdns, ak2_pattern)
        cdn = base64.b64decode(cdn).decode("utf-8")
        key = ''
        i = 0
        while(i < len(cdn)):
            key = key + chr(ord(cdn[i]) ^ ord(KEY_MASK[i % 8]))
            i = i + 1
        time_hex = hex(int(time.time()))[2:]
        key = hashlib.md5(bytes(key + "/zqlive/" + rtmp_id + time_hex, "utf-8")).hexdigest()
        real_url = rtmp_real_base + '/' + rtmp_id + "?k=" + key + "&t=" + time_hex
        print_info(site_info, title, 'flv', float('inf'))
        if not info_only:
            download_rtmp_url(real_url, title, 'flv', {}, output_dir, merge = merge)
            #download_urls([real_url], title, 'flv', None, output_dir, merge = merge)
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
