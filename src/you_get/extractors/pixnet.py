#!/usr/bin/env python

__all__ = ['pixnet_download']

from ..common import *
import urllib.error
from time import time
from urllib.parse import quote
from json import loads

def pixnet_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://(\w)+.pixnet.net/album/video/(\d)+', url):
        # http://eric6513.pixnet.net/album/video/206644535
        html = get_content(url)
        title = ''.join(r1(r'<meta property="og:description\" content="([^"]*)"', html).split('-')[1:]).strip()
        
        time_now = int(time())
        
        m = re.match(r'http://(\w+).pixnet.net/album/video/(\d+)', url)
        
        username = m.group(1)
        # eric6513
        id = m.group(2)
        # 206644535
        
        data_dict = {'username': username, 'autoplay': 1, 'id': id, 'loop': 0, 'profile': 9, 'time': time_now}
        data_dict_str= quote(str(data_dict).replace("'", '"'), safe='"')  #have to be like this
        url2 = 'http://api.pixnet.tv/content?type=json&customData=' + data_dict_str
        # &sig=edb07258e6a9ff40e375e11d30607983  can be blank for now
        # if required, can be obtained from url like
        # http://s.ext.pixnet.tv/user/eric6513/html5/autoplay/206644507.js
        # http://api.pixnet.tv/content?type=json&customData={%22username%22:%22eric6513%22,%22id%22:%22206644535%22,%22time%22:1441823350,%22autoplay%22:0,%22loop%22:0,%22profile%22:7}
        
        video_json = get_content(url2)
        content = loads(video_json)
        url_main = content['element']['video_url']
        url_backup = content['element']['backup_video_uri']
        # {"element":{"video_url":"http:\/\/cdn-akamai.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_6.mp4","backup_video_uri":"http:\/\/fet-1.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_6.mp4","thumb_url":"\/\/imageproxy.pimg.tw\/zoomcrop?width=480&height=360&url=http%3A%2F%2Fpimg.pixnet.tv%2Fuser%2Feric6513%2F206644507%2Fbg_000000%2F480x360%2Fdefault.jpg%3Fv%3D1422870050","profiles":{"360p":"http:\/\/cdn-akamai.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567.flv","480p":"http:\/\/cdn-akamai.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_2.mp4","720p":"http:\/\/cdn-akamai.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_3.mp4"},"backup_profiles":{"360p":"http:\/\/fet-1.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567.flv","480p":"http:\/\/fet-1.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_2.mp4","720p":"http:\/\/fet-1.node1.cache.pixnet.tv\/user\/eric6513\/13541121820567_3.mp4"},"count_play_url":["http:\/\/api.v6.pixnet.tv\/count?username=eric6513&amp;file=13541121820567.flv&amp;t=1441819681&amp;type=v6play&amp;sig=3350496782","http:\/\/api.pixnet.tv\/count?username=eric6513&amp;file=13541121820567.flv&amp;t=1441819681&amp;type=play&amp;sig=930187858","http:\/\/api.pixnet.tv\/count?username=eric6513&amp;file=13541121820567.flv&amp;t=1441819681&amp;type=html5play&amp;sig=4191197761"],"count_finish_url":["http:\/\/api.pixnet.tv\/count?username=eric6513&amp;file=13541121820567.flv&amp;t=1441819715&amp;type=finish&amp;sig=638797202","http:\/\/api.pixnet.tv\/count?username=eric6513&amp;file=13541121820567.flv&amp;t=1441819715&amp;type=html5finish&amp;sig=3215728991"]}}
        
        try:
            # In some rare cases the main URL is IPv6 only...
            # Something like #611
            url_info(url_main)
            url = url_main
        except:
            url = url_backup
        
        type, ext, size = url_info(url)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "Pixnet"
download = pixnet_download
download_playlist = playlist_not_supported('pixnet')
