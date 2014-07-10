#!/usr/bin/env python

__all__ = ['kugou_download']

from ..common import *
from json import loads
from base64 import b64decode


def kugou_download(url, output_dir=".", merge=True, info_only=False):
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
            download_urls([url], title, ext, size, output_dir)
    else:
        #for the www.kugou.com/
        raise NotImplementedError(url)       

site_info = "kugou.com"
download = kugou_download
download_playlist = playlist_not_supported("kugou")
