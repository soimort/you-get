#!/usr/bin/env python

__all__ = ['ucas_download', 'ucas_download_single', 'ucas_download_playlist']

from ..common import *
import urllib.error
import http.client
from time import time
from random import random
import xml.etree.ElementTree as ET
from copy import copy

"""
Do not replace http.client with get_content
for UCAS's server is not correctly returning data!
"""

def dictify(r,root=True):
    """http://stackoverflow.com/a/30923963/2946714"""
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d

def _get_video_query_url(resourceID):
    # has to be like this
    headers = {
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.47 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://v.ucas.ac.cn/',
        'Connection': 'keep-alive',
    }
    conn = http.client.HTTPConnection("210.76.211.10")
    
    conn.request("GET", "/vplus/remote.do?method=query2&loginname=videocas&pwd=af1c7a4c5f77f790722f7cae474c37e281203765d423a23b&resource=%5B%7B%22resourceID%22%3A%22" + resourceID + "%22%2C%22on%22%3A1%2C%22time%22%3A600%2C%22eid%22%3A100%2C%22w%22%3A800%2C%22h%22%3A600%7D%5D&timeStamp=" + str(int(time())), headers=headers)
    res = conn.getresponse()
    data = res.read()

    info =  data.decode("utf-8")
    return match1(info, r'video":"(.+)"')

def _get_virtualPath(video_query_url):
    #getResourceJsCode2
    html = get_content(video_query_url)
    
    return match1(html, r"function\s+getVirtualPath\(\)\s+{\s+return\s+'(\w+)'")


def _get_video_list(resourceID):
    """"""
    conn = http.client.HTTPConnection("210.76.211.10")
        
    conn.request("GET", '/vplus/member/resource.do?isyulan=0&method=queryFlashXmlByResourceId&resourceId={resourceID}&randoms={randoms}'.format(resourceID = resourceID,
                                                                                                                                            randoms = random()))
    res = conn.getresponse()
    data = res.read()

    video_xml = data.decode("utf-8")

    root = ET.fromstring(video_xml.split('___!!!___')[0])

    r = dictify(root)

    huge_list = []
    # main
    huge_list.append([i['value'] for i in sorted(r['video']['mainUrl'][0]['_flv'][0]['part'][0]['video'], key=lambda k: int(k['index']))])

    # sub
    if '_flv' in r['video']['subUrl'][0]:
        huge_list.append([i['value'] for i in sorted(r['video']['subUrl'][0]['_flv'][0]['part'][0]['video'], key=lambda k: int(k['index']))])

    return huge_list

def _ucas_get_url_lists_by_resourceID(resourceID):
    video_query_url = _get_video_query_url(resourceID)
    assert video_query_url != '', 'Cannot find video GUID!'
    
    virtualPath = _get_virtualPath(video_query_url)
    assert virtualPath != '', 'Cannot find virtualPath!'
    
    url_lists = _get_video_list(resourceID)
    assert url_lists, 'Cannot find any URL to download!'

    # make real url
    # credit to a mate in UCAS
    for video_type_id, video_urls in enumerate(url_lists):
        for k, path in enumerate(video_urls):
            url_lists[video_type_id][k] = 'http://210.76.211.10/vplus/member/resource.do?virtualPath={virtualPath}&method=getImgByStream&imgPath={path}'.format(virtualPath = virtualPath,
                                                                                                                                                                path = path)

    return url_lists

def ucas_download_single(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''video page'''
    html = get_content(url)
    # resourceID is UUID
    resourceID = re.findall( r'resourceID":"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html)[0]
    assert resourceID != '', 'Cannot find resourceID!'

    title = match1(html, r'<div class="bc-h">(.+)</div>')
    url_lists = _ucas_get_url_lists_by_resourceID(resourceID)
    assert url_lists, 'Cannot find any URL of such class!'
    
    for k, part in enumerate(url_lists):
        part_title = title + '_' + str(k)
        print_info(site_info, part_title, 'flv', 0)
        if not info_only:
            download_urls(part, part_title, 'flv', total_size=None, output_dir=output_dir, merge=merge)

def ucas_download_playlist(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''course page'''
    html = get_content(url)

    parts = re.findall( r'(getplaytitle.do\?.+)"', html)
    assert parts, 'No part found!'

    for part_path in parts:
        ucas_download('http://v.ucas.ac.cn/course/' + part_path, output_dir=output_dir, merge=merge, info_only=info_only)

def ucas_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if 'classid=' in url and 'getplaytitle.do' in url:
        ucas_download_single(url, output_dir=output_dir, merge=merge, info_only=info_only)
    elif 'CourseIndex.do' in url:
        ucas_download_playlist(url, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "UCAS"
download = ucas_download
download_playlist = ucas_download_playlist