#!/usr/bin/env python

__all__ = ['kuwo_download']

from ..common import *
import re

def kuwo_download_by_rid(rid, output_dir = '.', merge = True, info_only = False):
    html=get_content("http://player.kuwo.cn/webmusic/st/getNewMuiseByRid?rid=MUSIC_%s"%rid)
    title=match1(html,r"<name>(.*)</name>")
    #to get title
    #format =aac|mp3 ->to get aac format=mp3 ->to get mp3
    url=get_content("http://antiserver.kuwo.cn/anti.s?format=mp3&rid=MUSIC_%s&type=convert_url&response=url"%rid)
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir)

def kuwo_playlist_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html=get_content(url)
    matched=set(re.compile("yinyue/(\d+)").findall(html))#reduce duplicated
    for rid in matched:
        kuwo_download_by_rid(rid,output_dir,merge,info_only)



def kuwo_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if "www.kuwo.cn/yinyue" in url:
        rid=match1(url,'yinyue/(\d+)')
        kuwo_download_by_rid(rid,output_dir, merge, info_only)
    else:
        kuwo_playlist_download(url,output_dir,merge,info_only)

site_info = "kuwo.cn"
download = kuwo_download
# download_playlist = playlist_not_supported("kugou")
# download_playlist=playlist_not_supported("kuwo")
download_playlist=kuwo_playlist_download
