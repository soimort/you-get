#!/usr/bin/env python

__all__ = ['freebuf_download']

from ..common import *
from .le import letvcloud_download_by_vu
from .qq import qq_download
from .youku import youku_download_by_vid
from .tudou import tudou_download_by_id

import json, re

def freebuf_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    title=''
    source=''
    vid=''
    videolink=''
    if re.match(r'^http://www.freebuf.com/.*',url):
        title=match1(html,r'<div class="title">[^<>]+<h2>[ ]*([^<>]+)[ ]*<')
        videolink=match1(html,r'<iframe[^<>]+src="([^"]+)"') or \
                  match1(html,r'<embed[^<>]+src="([^"]+)"')
        vid=match1(videolink,r'vid=([0-9a-zA-Z]+)') or \
            match1(videolink, r'player\.youku\.com/embed/([a-zA-Z0-9=]+)') or \
            match1(videolink,r'http://www.tudou.com/v/([^/]+)/')
        source=getSourceByLink(videolink)
    elif re.match(r'http://open.freebuf.com/.*',url):
        title=match1(html,r'class="entry-title"[^>]*>([^<>]+)<')
        uu=match1(html,r'"uu":"([0-9a-zA-Z]+)"')
        vu=match1(html,r'"vu":"([0-9a-zA-Z]+)"')
        if uu and vu:
            source='letv'
        else:
            videolink=match1(html,r'<iframe[^<>]+src="([^"]+)"')
            source=getSourceByLink(videolink)
            vid=match1(videolink,r'vid=([0-9a-zA-Z]+)') or \
                match1(videolink, r'player\.youku\.com/embed/([a-zA-Z0-9=]+)')
    else:
        raise NotImplementedError("url not included")
    if source=='qq':
        qq_download(videolink, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
    elif source=='letv':
        letvcloud_download_by_vu(vu, uu, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif source=='youku':
        youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
    elif source=='tudou':
        tudou_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        raise NotImplementedError(source)

def getSourceByLink(link):
    source='None'
    tail=1
    while source!='qq' and source!='youku' and source!='tudou' and tail<4:
        try:
            source=re.search(r'http://(\w+)\.(\w+)\.(\w+)',link).group(tail)
        except:
            return source
        tail+=1
    return source

site_info = "FREEBUF.com"
download = freebuf_download
download_playlist = playlist_not_supported('freebuf')

