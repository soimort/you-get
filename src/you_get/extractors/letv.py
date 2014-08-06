#!/usr/bin/env python

__all__ = ['letv_download']

import json
import random
import xml.etree.ElementTree as ET
from ..common import *

def get_timestamp():
    tn = random.random()
    url = 'http://api.letv.com/time?tn={}'.format(tn)
    result = get_content(url)
    return json.loads(result)['stime']

def get_key(t):
    for s in range(0, 8):
        e = 1 & t
        t >>= 1
        e <<= 31
        t += e
    return t ^ 185025305


def video_info(vid):
    tn = get_timestamp()
    key = get_key(tn)
#old api reserve for future use or for example
    # url = 'http://api.letv.com/mms/out/video/play?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(vid, key)
    # print(url)
    # r = get_content(url, decoded=False)
    # print(r)
    # xml_obj = ET.fromstring(r)
    # info = json.loads(xml_obj.find("playurl").text)
    # title = info.get('title')
    # urls = info.get('dispatch')
    # for k in urls.keys():
    #     url = urls[k][0]
    #     break
    # url += '&termid=1&format=0&hwtype=un&ostype=Windows7&tag=letv&sign=letv&expect=1&pay=0&rateid={}'.format(k)
    # return url, title


    url="http://api.letv.com/mms/out/common/geturl?platid=3&splatid=301&playid=0&vtype=9,13,21,28&version=2.0&tss=no&vid={}&domain=www.letv.com&tkey={}".format(vid,key)
    r = get_content(url, decoded=False)
    info=json.loads(str(r,"utf-8"))
    size=0
    for i in info["data"][0]["infos"]: #0 means only one file not truncated.need to upgrade 
        if int(i["gsize"])>size:
            size=int(i["gsize"])
            url=i["mainUrl"]

    url+="&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=Linux&tag=letv&sign=letv&expect=3&tn={}&pay=0&iscpn=f9051&rateid=1300".format(random.random())
    # url += '&termid=1&format=0&hwtype=un&ostype=Windows7&tag=letv&sign=letv&expect=1&pay=0&rateid=1000'   #{}'.format(k)
    r2=get_content(url,decoded=False)
    info2=json.loads(str(r2,"utf-8"))
    return info2["location"]

    # return url

def letv_download_by_vid(vid,title, output_dir='.', merge=True, info_only=False):
    url= video_info(vid)
    _, _, size = url_info(url)
    ext = 'flv'
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def letv_download(url, output_dir='.', merge=True, info_only=False):
    html = get_content(url)
    #to get title
    if re.match(r'http://www.letv.com/ptv/vplay/(\d+).html', url):
        vid = match1(url, r'http://www.letv.com/ptv/vplay/(\d+).html')
    else:
        vid = match1(html, r'vid="(\d+)"')
    title=match1(html,r'name="irTitle" content="(.*?)"')
    letv_download_by_vid(vid,title, output_dir=output_dir, merge=merge, info_only=info_only)


site_info = "letv.com"
download = letv_download
download_playlist = playlist_not_supported('letv')
