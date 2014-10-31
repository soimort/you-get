#!/usr/bin/env python

__all__ = ['letvcloud_download', 'letvcloud_download_by_vu']

from ..common import *
import urllib.request
import json
import hashlib
import base64

def letvcloud_download_by_vu(vu, title = None, output_dir = '.', merge = True, info_only = False):
    str2Hash = 'cfflashformatjsonran0.7214574650861323uu2d8c027396ver2.1vu' + vu + 'bie^#@(%27eib58'
    sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
    request_info = urllib.request.Request('http://api.letvcloud.com/gpc.php?&sign='+sign+'&cf=flash&vu='+vu+'&ver=2.1&ran=0.7214574650861323&qr=2&format=json&uu=2d8c027396')
    #response = urllib.request.urlopen(request_info)
    #data = response.read()
    #info = json.loads(data.decode('utf-8'))
    #type_available = []
    #for i in info['data']['video_info']['media']:
    #    type_available.append({'video_url': info['data']['video_info']['media'][i]['play_url']['main_url'], 'video_quality': int(info['data']['video_info']['media'][i]['play_url']['vtype'])})
    #url = [base64.b64decode(sorted(type_available ,key = lambda x:x['video_quality'])[-1]['video_url'])]
    #print(url)#
    #exit(0)#
    try:
        response = urllib.request.urlopen(request_info)
        data = response.read()
        info = json.loads(data.decode('utf-8'))
        type_available = []
        if info['code'] == 0:
            for i in info['data']['video_info']['media']:
                type_available.append({'video_url': info['data']['video_info']['media'][i]['play_url']['main_url'], 'video_quality': int(info['data']['video_info']['media'][i]['play_url']['vtype'])})
            url = [base64.b64decode(sorted(type_available, key = lambda x:x['video_quality'])[-1]['video_url'])]
        else:
            raise ValueError('Cannot get URL!')
    except:
        print('ERROR: Cannot get video URL!')
    #\mp4\
    download_urls([url], title, ext, size, output_dir, merge = merge)

#site_info = "Letvcloud"
#download = letvcloud_download
#download_playlist = playlist_not_supported('letvcloud')
