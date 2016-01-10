#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .letv import letvcloud_download_by_vu
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_vid

import json, re

def get_srt_json(id):
    url = 'http://danmu.aixifan.com/V2/%s' % id
    return get_html(url)

def acfun_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False, **kwargs):
    info = json.loads(get_html('http://www.acfun.tv/video/getVideo.aspx?id=' + vid))
    sourceType = info['sourceType']
    if 'sourceId' in info: sourceId = info['sourceId']
    # danmakuId = info['danmakuId']
    if sourceType == 'sina':
        sina_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'youku':
        youku_download_by_vid(sourceId, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'tudou':
        tudou_download_by_iid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'qq':
        qq_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'letv':
        letvcloud_download_by_vu(sourceId, '2d8c027396', title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'zhuzhan':
        a = 'http://api.aixifan.com/plays/%s/realSource' % vid
        s = json.loads(get_content(a, headers={'deviceType': '1'}))
        urls = s['data']['files'][-1]['url']
        size = urls_size(urls)
        print_info(site_info, title, 'mp4', size)
        if not info_only:
            download_urls(urls, title, 'mp4', size,
                          output_dir=output_dir, merge=merge)
    else:
        raise NotImplementedError(sourceType)

    if not info_only and not dry_run:
        if not kwargs['caption']:
            print('Skipping danmaku.')
            return
        try:
            title = get_filename(title)
            print('Downloading %s ...\n' % (title + '.cmt.json'))
            cmt = get_srt_json(vid)
            with open(os.path.join(output_dir, title + '.cmt.json'), 'w', encoding='utf-8') as x:
                x.write(cmt)
        except:
            pass

def acfun_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    assert re.match(r'http://[^\.]+.acfun.[^\.]+/\D/\D\D(\d+)', url)
    html = get_html(url)

    title = r1(r'<h1 id="txt-title-view">([^<>]+)<', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    assert title

    videos = re.findall("data-vid=\"(\d+)\".*href=\"[^\"]+\".*title=\"([^\"]+)\"", html)
    for video in videos:
        p_vid = video[0]
        p_title = title + " - " + video[1] if video[1] != '删除标签' else title
        acfun_download_by_vid(p_vid, p_title,
                              output_dir=output_dir,
                              merge=merge,
                              info_only=info_only,
                              **kwargs)

site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
