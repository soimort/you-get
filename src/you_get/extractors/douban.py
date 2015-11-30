#!/usr/bin/env python

__all__ = ['douban_download']

import urllib.request, urllib.parse
from ..common import *

def douban_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html(url)
    if 'subject' in url:
        titles = re.findall(r'data-title="([^"]*)">', html)
        song_id = re.findall(r'<li class="song-item" id="([^"]*)"', html)
        song_ssid = re.findall(r'data-ssid="([^"]*)"', html)
        get_song_url = 'http://music.douban.com/j/songlist/get_song_url'
        
        for i in range(len(titles)):
            title = titles[i]
            datas = {
                'sid': song_id[i],
                'ssid': song_ssid[i]
            }
            post_params = urllib.parse.urlencode(datas).encode('utf-8')
            try:
                resp = urllib.request.urlopen(get_song_url, post_params)
                resp_data = json.loads(resp.read().decode('utf-8'))
                real_url = resp_data['r']
                type, ext, size = url_info(real_url)
                print_info(site_info, title, type, size)
            except:
                pass

            if not info_only:
                try:
                    download_urls([real_url], title, ext, size, output_dir, merge = merge)
                except:
                    pass

    else: 
        titles = re.findall(r'"name":"([^"]*)"', html)
        real_urls = [re.sub('\\\\/', '/', i) for i in re.findall(r'"rawUrl":"([^"]*)"', html)]
        
        for i in range(len(titles)):
            title = titles[i]
            real_url = real_urls[i]
            
            type, ext, size = url_info(real_url)
            
            print_info(site_info, title, type, size)
            if not info_only:
                download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Douban.com"
download = douban_download
download_playlist = playlist_not_supported('douban')
