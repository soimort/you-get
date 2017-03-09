#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .le import letvcloud_download_by_vu
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_vid, youku_open_download_by_vid

import json, re

def get_srt_json(id):
    url = 'http://danmu.aixifan.com/V2/%s' % id
    return get_html(url)

def acfun_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False, **kwargs):
    """str, str, str, bool, bool ->None

    Download Acfun video by vid.

    Call Acfun API, decide which site to use, and pass the job to its
    extractor.
    """

    #first call the main parasing API
    info = json.loads(get_html('http://www.acfun.tv/video/getVideo.aspx?id=' + vid))

    sourceType = info['sourceType']

    #decide sourceId to know which extractor to use
    if 'sourceId' in info: sourceId = info['sourceId']
    # danmakuId = info['danmakuId']

    #call extractor decided by sourceId
    if sourceType == 'sina':
        sina_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'youku':
        youku_download_by_vid(sourceId, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
    elif sourceType == 'tudou':
        tudou_download_by_iid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'qq':
        qq_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'letv':
        letvcloud_download_by_vu(sourceId, '2d8c027396', title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'zhuzhan':
        #As in Jul.28.2016, Acfun is using embsig to anti hotlink so we need to pass this
        embsig =  info['encode']
        a = 'http://api.aixifan.com/plays/%s' % vid
        s = json.loads(get_content(a, headers={'deviceType': '2'}))
        if s['data']['source'] == "zhuzhan-youku":
            sourceId = s['data']['sourceId']
            youku_open_download_by_vid(client_id='908a519d032263f8', vid=sourceId, title=title, output_dir=output_dir,merge=merge, info_only=info_only, embsig = embsig, **kwargs)
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

    title = r1(r'data-title="([^"]+)"', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    assert title
    if match1(url, r'_(\d+)$'): # current P
        title = title + " " + r1(r'active">([^<]*)', html)

    vid = r1('data-vid="(\d+)"', html)
    up = r1('data-name="([^"]+)"', html)
    title = title + ' - ' + up
    acfun_download_by_vid(vid, title,
                          output_dir=output_dir,
                          merge=merge,
                          info_only=info_only,
                          **kwargs)

site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
