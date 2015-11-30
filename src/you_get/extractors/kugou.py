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
    else:
        #for the www.kugou.com/
        return kugou_download_playlist(url, output_dir=output_dir, merge=merge, info_only=info_only)
        # raise NotImplementedError(url)       

def kugou_download_by_hash(title,hash_val,output_dir = '.', merge = True, info_only = False):
    #sample
    #url_sample:http://www.kugou.com/yy/album/single/536957.html
    #hash ->key  md5(hash+kgcloud")->key  decompile swf
    #cmd 4 for mp3 cmd 3 for m4a
    key=hashlib.new('md5',(hash_val+"kgcloud").encode("utf-8")).hexdigest()
    html=get_html("http://trackercdn.kugou.com/i/?pid=6&key=%s&acceptMp3=1&cmd=4&hash=%s"%(key,hash_val))
    j=loads(html)
    url=j['url']
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

def kugou_download_playlist(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html=get_html(url)
    pattern=re.compile('title="(.*?)".* data="(\w*)\|.*?"')
    pairs=pattern.findall(html)
    for title,hash_val in pairs:
        kugou_download_by_hash(title,hash_val,output_dir,merge,info_only)


site_info = "kugou.com"
download = kugou_download
# download_playlist = playlist_not_supported("kugou")
download_playlist=kugou_download_playlist
