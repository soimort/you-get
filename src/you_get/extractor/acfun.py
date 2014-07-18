#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .qq import qq_download_by_id
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_vid

import json, re

def get_srt_json(id):
    url = 'http://comment.acfun.tv/%s.json' % id
    return get_html(url)

def get_srt_lock_json(id):
    url = 'http://comment.acfun.tv/%s_lock.json' % id
    return get_html(url)

def acfun_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False):
    info = json.loads(get_html('http://www.acfun.tv/video/getVideo.aspx?id=' + vid))
    sourceType = info['sourceType']
    sourceId = info['sourceId']
    danmakuId = info['danmakuId']
    if sourceType == 'sina':
        sina_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'youku':
        youku_download_by_vid(sourceId, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'tudou':
        tudou_download_by_iid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'qq':
        qq_download_by_id(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        raise NotImplementedError(sourceType)

    if not info_only:
        title = get_filename(title)
        try:
            print('Downloading %s ...\n' % (title + '.cmt.json'))
            cmt = get_srt_json(danmakuId)
            with open(os.path.join(output_dir, title + '.cmt.json'), 'w') as x:
                x.write(cmt)
            print('Downloading %s ...\n' % (title + '.cmt_lock.json'))
            cmt = get_srt_lock_json(danmakuId)
            with open(os.path.join(output_dir, title + '.cmt_lock.json'), 'w') as x:
                x.write(cmt)
        except:
            pass

def acfun_download(url, output_dir = '.', merge = True, info_only = False):
    assert re.match(r'http://[^\.]+.acfun.[^\.]+/v/ac(\d+)', url)
    html = get_html(url)

    title = r1(r'<h1 id="txt-title-view">([^<>]+)<', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    assert title

    videos = re.findall("data-vid=\"(\d+)\" href=\"[^\"]+\" title=\"([^\"]+)\"", html)
    if videos is not None:
        for video in videos:
            p_vid = video[0]
            p_title = title + " - " + video[1]
            acfun_download_by_vid(p_vid, p_title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        # Useless - to be removed?
        id = r1(r"src=\"/newflvplayer/player.*id=(\d+)", html)
        sina_download_by_vid(id, title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
