#!/usr/bin/env python

__all__ = ['lizhi_download']
import json
from ..common import *

def lizhi_download_playlist(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    # like this http://www.lizhi.fm/#/31365/
    #api desc: s->start l->length band->some radio
    #http://www.lizhi.fm/api/radio_audios?s=0&l=100&band=31365
    band_id = match1(url,r'#/(\d+)')
    #try to get a considerable large l to reduce html parsing task.
    api_url = 'http://www.lizhi.fm/api/radio_audios?s=0&l=65535&band='+band_id
    content_json = json.loads(get_content(api_url))
    for sound in content_json:
        title = sound["name"]
        res_url = sound["url"]
        songtype, ext, size = url_info(res_url,faker=True)
        print_info(site_info, title, songtype, size)
        if not info_only:
            #no referer no speed!
            download_urls([res_url], title, ext, size, output_dir, merge=merge ,refer = 'http://www.lizhi.fm',faker=True)    
    pass

def lizhi_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    # url like http://www.lizhi.fm/#/549759/18864883431656710
    api_id = match1(url,r'#/(\d+/\d+)')
    api_url = 'http://www.lizhi.fm/api/audio/'+api_id
    content_json = json.loads(get_content(api_url))
    title = content_json["audio"]["name"]
    res_url = content_json["audio"]["url"]
    songtype, ext, size = url_info(res_url,faker=True)
    print_info(site_info, title, songtype, size)
    if not info_only:
        #no referer no speed!
        download_urls([res_url], title, ext, size, output_dir, merge=merge ,refer = 'http://www.lizhi.fm',faker=True)    


site_info = "lizhi.fm"
download = lizhi_download
download_playlist = lizhi_download_playlist
