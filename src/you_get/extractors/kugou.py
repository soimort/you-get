#!/usr/bin/env python

__all__ = ['kugou_download']

from ..common import *
from json import loads
from base64 import b64decode
import re
import hashlib

def kugou_download(url, output_dir=".", merge=True, info_only=False, **kwargs):
    if url.lower().find("5sing")!=-1:
        #for 5sing.kugou.com
        html=get_html(url)
        ticket=r1(r'"ticket":\s*"(.*)"',html)
        j=loads(str(b64decode(ticket),encoding="utf-8"))
        url=j['file']
        title=j['songName']
        songtype, ext, size = url_info(url)
        print_info(site_info, title, songtype, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir, merge=merge)
    elif url.lower().find("hash")!=-1:
        return kugou_download_by_hash(url,output_dir,merge,info_only)
    else:
        #for the www.kugou.com/
        return kugou_download_playlist(url, output_dir=output_dir, merge=merge, info_only=info_only)
        # raise NotImplementedError(url)       


def kugou_download_by_hash(url,output_dir = '.', merge = True, info_only = False):
    #sample
    #url_sample:http://www.kugou.com/song/#hash=93F7D2FC6E95424739448218B591AEAF&album_id=9019462
    hash_val = match1(url,'hash=(\w+)')
    album_id = match1(url,'album_id=(\d+)')
    html = get_html("http://www.kugou.com/yy/index.php?r=play/getdata&hash={}&album_id={}".format(hash_val,album_id))
    j =loads(html)
    url = j['data']['play_url']
    title = j['data']['audio_name']
    # some songs cann't play because of copyright protection
    if(url == ''):
        return
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

def kugou_download_playlist(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    urls=[]
    
    #download music leaderboard
    #sample: http://www.kugou.com/yy/html/rank.html
    if url.lower().find('rank') !=-1:
        html=get_html(url)
        pattern = re.compile('<a href="(http://.*?)" data-active=')
        res = pattern.findall(html)
        for song in res:
            res = get_html(song)
            pattern_url = re.compile('"hash":"(\w+)".*"album_id":(\d)+')
            hash_val,album_id= res = pattern_url.findall(res)[0]
            urls.append('http://www.kugou.com/song/#hash=%s&album_id=%s'%(hash_val,album_id))
    
    # download album
    # album sample:   http://www.kugou.com/yy/album/single/1645030.html
    elif url.lower().find('album')!=-1:
        html = get_html(url)
        pattern = re.compile('var data=(\[.*?\]);')
        res = pattern.findall(html)[0]
        for v in json.loads(res):
            urls.append('http://www.kugou.com/song/#hash=%s&album_id=%s'%(v['hash'],v['album_id']))

    # download the playlist        
    # playlist sample:http://www.kugou.com/yy/special/single/487279.html
    else:
        html = get_html(url)
        pattern = re.compile('data="(\w+)\|(\d+)"')
        for v in pattern.findall(html):
            urls.append('http://www.kugou.com/song/#hash=%s&album_id=%s'%(v[0],v[1]))
            print('http://www.kugou.com/song/#hash=%s&album_id=%s'%(v[0],v[1]))

    #download the list by hash
    for url in urls:
        kugou_download_by_hash(url,output_dir,merge,info_only)

                

site_info = "kugou.com"
download = kugou_download
# download_playlist = playlist_not_supported("kugou")
download_playlist=kugou_download_playlist
