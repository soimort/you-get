#!/usr/bin/env python

__all__ = ['longzhu_download']

from ..common import *
import json

def longzhu_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    web_domain = url.split("/")[2]
    if (web_domain == 'star.longzhu.com') or (web_domain == 'y.longzhu.com'):
        domain = url.split('/')[3].split('?')[0]
        m_url = "http://m.longzhu.com/%s" % domain
        m_html = get_content(m_url)
        room_id_patt = r'var\s*roomId\s*=\s*(\d+);'
        room_id = match1(m_html,room_id_patt)

        json_url = "http://liveapi.plu.cn/liveapp/roomstatus?roomId=%s" % room_id
        content = get_html(json_url)
        data = json.loads(content)
        streamUri = data['streamUri']
        if len(streamUri) <= 4:
            raise ValueError("The live stream is not online!")
        title = data['title']
        streamer = data ['userName']
        title = streamer + ": " + title
        
        steam_api_url = "http://livestream.plu.cn/live/getlivePlayurl?roomId=%s" % room_id
        content = get_content(steam_api_url)
        data = json.loads(content)
        isonline = data.get('isTransfer')
        if isonline == '0':
            raise ValueError("The live stream is not online!")
            
        default_rate = data.get('defaultRateLevel')
        urls = data['playLines'][0]['urls']
        for s in urls:
            if s['rateLevel'] == default_rate and s['ext'] == 'flv':
                real_url = s['securityUrl']
                break
        else:real_url = urls[0]['securityUrl']
        
        print_info(site_info, title, 'flv', float('inf'))
 
        if not info_only:
            download_urls([real_url], title, 'flv', None, output_dir, merge = merge)
            
    elif web_domain == 'replay.longzhu.com':
        videoid = match1(url, r'(\d+)$')
        json_url = "http://liveapi.longzhu.com/livereplay/getreplayfordisplay?videoId=%s" % videoid
        content = get_content(json_url)
        data = json.loads(content)
        
        username = data['userName']
        title = data['title']
        title = username + ": " + title
        real_url = data['videoUrl']
        
        if player:
            print_info('Longzhu Video', title, 'm3u8', 0)
            download_urls([real_url], title, 'm3u8', 0, output_dir, merge = merge)
        else:
            urls = general_m3u8_extractor(real_url)
            print_info('Longzhu Video', title, 'm3u8', 0)
            if not info_only:
                download_urls(urls, title, 'ts', 0, output_dir=output_dir, merge=merge, **kwargs)

    else:
        raise ValueError("Wrong url or unsupported link ... %s" % url) 

site_info = "longzhu.com"
download = longzhu_download
download_playlist = playlist_not_supported('longzhu')
