#!/usr/bin/env python

__all__ = ['longzhu_download']

from ..common import *
import json

   
def longzhu_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    host_name = url.split("/")[2]

    if host_name == 'star.longzhu.com' or host_name == 'm.longzhu.com':
        domain_param = url.split('/')[3].split('?')[0]
        get_id_url = "http://m.longzhu.com/%s" % domain_param
        html = get_content(get_id_url)
        room_id_patt = r'var\s+roomId\s*=\s*(\d+);'  #var roomId = 394548;
        room_id = match1(html, room_id_patt)

        json_request_url = "http://liveapi.plu.cn/liveapp/roomstatus?roomId=%s" % room_id
        content = get_html(json_request_url)
        data = json.loads(content)
        streamUri = data['streamUri']
        if len(streamUri) <= 4:
            raise ValueError("The live stream is not online!")
        title = data['title']
        streamer = data ['userName']
        title = streamer + ": " + title
        
        json_request_url = "http://livestream.plu.cn/live/getlivePlayurl?roomId=%s" % room_id
        content = get_content(json_request_url)
        data = json.loads(content)
        default_rate = data.get('defaultRateLevel')
        urls = data['playLines'][0]['urls']
        for s in urls:
            if s['rateLevel'] == default_rate and s['ext'] == 'flv':
                real_url = s['securityUrl']
                break
        else:real_url = urls[0]['securityUrl']
        
        site_info = "star.longzhu.com"
        print_info(site_info, title, 'flv', float('inf'))
        
        if not info_only:
            download_urls([real_url], title, 'flv', None, output_dir, merge = merge)
            
    elif host_name == 'yoyo.longzhu.com':
        html = get_content(url)

        status_patt = r'"isLive"\s*:\s*(false|true)\s*,'
        status = match1(html, status_patt)

        if status == 'false': #get offline video url
            offlineVideo_patt = r'"offlineVideoUrl":"([^"]*)",'
            offlineVideo_url = match1(html, offlineVideo_patt).replace('\\','')

        title_patt = r'<title>([^<]{1,9999})</title>'
        title = match1(html, title_patt)

        site_info = "yoyo.longzhu.com"
        
        if status == 'true':
            real_url_patt = r'"rtmpUrl"\s*:\s*"([^"]+)",'
            real_url = match1(html, real_url_patt).replace('\\','')
            print_info(site_info, title, 'rtmp', float('inf'))
            if not info_only:
                #download_urls([real_url], title, 'mp4', None, output_dir, merge = merge)
                download_url_ffmpeg(real_url, title, 'flv', {}, output_dir = output_dir, merge = merge)

        elif len(offlineVideo_url) >= 4 :
            real_url = offlineVideo_url
            title += " --offline video-- "
            print_info(site_info, title, 'flv', float('inf'))
            if not info_only:
                download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

        else:
            raise ValueError ("The live stream is not online, and no offline Video!")

    else:
        raise ValueError("Wrong url or unsupported link ... %s" % url) #only star,m and yoyo,three avaliable child sites of longzhu.com

download = longzhu_download
download_playlist = playlist_not_supported('longzhu')