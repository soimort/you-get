#!/usr/bin/env python

__all__ = ['letv_download', 'letvcloud_download', 'letvcloud_download_by_vu']

import json
import random
import xml.etree.ElementTree as ET
import base64, hashlib, urllib, time, re

from ..common import *

#@DEPRECATED 
def get_timestamp():
    tn = random.random()
    url = 'http://api.letv.com/time?tn={}'.format(tn)
    result = get_content(url)
    return json.loads(result)['stime']
#@DEPRECATED 
def get_key(t):
    for s in range(0, 8):
        e = 1 & t
        t >>= 1
        e <<= 31
        t += e
    return t ^ 185025305

def calcTimeKey(t):
    ror = lambda val, r_bits, : ((val & (2**32-1)) >> r_bits%32) |  (val << (32-(r_bits%32)) & (2**32-1))
    return ror(ror(t,773625421%13)^773625421,773625421%17)


def decode(data):
    version = data[0:5]
    if version.lower() == b'vc_01':
        #get real m3u8
        loc2 = data[5:]
        length = len(loc2)
        loc4 = [0]*(2*length)
        for i in range(length):
            loc4[2*i] = loc2[i] >> 4
            loc4[2*i+1]= loc2[i] & 15;
        loc6 = loc4[len(loc4)-11:]+loc4[:len(loc4)-11]
        loc7 = [0]*length
        for i in range(length):
            loc7[i] = (loc6[2 * i] << 4) +loc6[2*i+1]
        return ''.join([chr(i) for i in loc7])
    else:
        # directly return
        return data



  
def video_info(vid,**kwargs):
    url = 'http://api.letv.com/mms/out/video/playJson?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(vid,calcTimeKey(int(time.time())))
    r = get_content(url, decoded=False)
    info=json.loads(str(r,"utf-8"))


    stream_id = None
    support_stream_id = info["playurl"]["dispatch"].keys()
    if "stream_id" in kwargs and kwargs["stream_id"].lower() in support_stream_id:
        stream_id = kwargs["stream_id"]
    else:
        print("Current Video Supports:")
        for i in support_stream_id:
            print("\t--format",i,"<URL>")
        if "1080p" in support_stream_id:
            stream_id = '1080p'
        elif "720p" in support_stream_id:
            stream_id = '720p'
        else:
            stream_id =sorted(support_stream_id,key= lambda i: int(i[1:]))[-1]

    url =info["playurl"]["domain"][0]+info["playurl"]["dispatch"][stream_id][0]
    ext = info["playurl"]["dispatch"][stream_id][1].split('.')[-1]
    url+="&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=Linux&tag=letv&sign=letv&expect=3&tn={}&pay=0&iscpn=f9051&rateid={}".format(random.random(),stream_id)

    r2=get_content(url,decoded=False)
    info2=json.loads(str(r2,"utf-8"))

    # hold on ! more things to do
    # to decode m3u8 (encoded)
    m3u8 = get_content(info2["location"],decoded=False)
    m3u8_list = decode(m3u8)
    urls = re.findall(r'^[^#][^\r]*',m3u8_list,re.MULTILINE)
    return ext,urls

def letv_download_by_vid(vid,title, output_dir='.', merge=True, info_only=False,**kwargs):
    ext , urls = video_info(vid,**kwargs)
    size = 0
    for i in urls:
        _, _, tmp = url_info(i)
        size += tmp

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir=output_dir, merge=merge)

def letvcloud_download_by_vu(vu, uu, title=None, output_dir='.', merge=True, info_only=False):
    #ran = float('0.' + str(random.randint(0, 9999999999999999))) # For ver 2.1
    #str2Hash = 'cfflashformatjsonran{ran}uu{uu}ver2.2vu{vu}bie^#@(%27eib58'.format(vu = vu, uu = uu, ran = ran)  #Magic!/ In ver 2.1
    argumet_dict ={'cf' : 'flash', 'format': 'json', 'ran': str(int(time.time())), 'uu': str(uu),'ver': '2.2', 'vu': str(vu), }
    sign_key = '2f9d6924b33a165a6d8b5d3d42f4f987'  #ALL YOUR BASE ARE BELONG TO US
    str2Hash = ''.join([i + argumet_dict[i] for i in sorted(argumet_dict)]) + sign_key
    sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
    request_info = urllib.request.Request('http://api.letvcloud.com/gpc.php?' + '&'.join([i + '=' + argumet_dict[i] for i in argumet_dict]) + '&sign={sign}'.format(sign = sign))
    response = urllib.request.urlopen(request_info)
    data = response.read()
    info = json.loads(data.decode('utf-8'))
    type_available = []
    for video_type in info['data']['video_info']['media']:
        type_available.append({'video_url': info['data']['video_info']['media'][video_type]['play_url']['main_url'], 'video_quality': int(info['data']['video_info']['media'][video_type]['play_url']['vtype'])})
    urls = [base64.b64decode(sorted(type_available, key = lambda x:x['video_quality'])[-1]['video_url']).decode("utf-8")]
    size = urls_size(urls)
    ext = 'mp4'
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir=output_dir, merge=merge)

def letvcloud_download(url, output_dir='.', merge=True, info_only=False):
    for i in url.split('&'):
        if 'vu=' in i:
            vu = i[3:]
        if 'uu=' in i:
            uu = i[3:]
    if len(vu) == 0:
        raise ValueError('Cannot get vu!')
    if len(uu) == 0:
        raise ValueError('Cannot get uu!')
    title = "LETV-%s" % vu
    letvcloud_download_by_vu(vu, uu, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

def letv_download(url, output_dir='.', merge=True, info_only=False ,**kwargs):
    if re.match(r'http://yuntv.letv.com/', url):
        letvcloud_download(url, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        html = get_content(url)
        #to get title
        if re.match(r'http://www.letv.com/ptv/vplay/(\d+).html', url):
            vid = match1(url, r'http://www.letv.com/ptv/vplay/(\d+).html')
        else:
            vid = match1(html, r'vid="(\d+)"')
        title = match1(html,r'name="irTitle" content="(.*?)"')
        letv_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only,**kwargs)

site_info = "LeTV.com"
download = letv_download
download_playlist = playlist_not_supported('letv')
