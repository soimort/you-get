#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .le import letvcloud_download_by_vu
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_vid

import json
import re
import base64
import time

def get_srt_json(id):
    url = 'http://danmu.aixifan.com/V2/%s' % id
    return get_content(url)

def youku_acfun_proxy(vid, sign, ref):
    endpoint = 'http://player.acfun.cn/flash_data?vid={}&ct=85&ev=3&sign={}&time={}'
    url = endpoint.format(vid, sign, str(int(time.time() * 1000)))
    json_data = json.loads(get_content(url, headers=dict(referer=ref)))['data']
    enc_text = base64.b64decode(json_data)
    dec_text = rc4(b'8bdc7e1a', enc_text).decode('utf8')
    youku_json = json.loads(dec_text)

    yk_streams = {}
    for stream in youku_json['stream']:
        tp = stream['stream_type']
        yk_streams[tp] = [], stream['total_size']
        if stream.get('segs'):
            for seg in stream['segs']:
                yk_streams[tp][0].append(seg['url'])
        else:
            yk_streams[tp] = stream['m3u8'], stream['total_size']

    return yk_streams

def acfun_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False, **kwargs):
    """str, str, str, bool, bool ->None

    Download Acfun video by vid.

    Call Acfun API, decide which site to use, and pass the job to its
    extractor.
    """

    #first call the main parasing API
    info = json.loads(get_content('http://www.acfun.cn/video/getVideo.aspx?id=' + vid))

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
        qq_download_by_vid(sourceId, title, True, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'letv':
        letvcloud_download_by_vu(sourceId, '2d8c027396', title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'zhuzhan':
        #As in Jul.28.2016, Acfun is using embsig to anti hotlink so we need to pass this
#In Mar. 2017 there is a dedicated ``acfun_proxy'' in youku cloud player
#old code removed
        url = 'http://www.acfun.cn/v/ac' + vid
        yk_streams = youku_acfun_proxy(info['sourceId'], info['encode'], url)
        seq = ['mp4hd3', 'mp4hd2', 'mp4hd', 'flvhd']
        for t in seq:
            if yk_streams.get(t):
                preferred = yk_streams[t]
                break
#total_size in the json could be incorrect(F.I. 0)
        size = 0
        for url in preferred[0]:
            _, _, seg_size = url_info(url)
            size += seg_size
#fallback to flvhd is not quite possible
        if re.search(r'fid=[0-9A-Z\-]*.flv', preferred[0][0]):
            ext = 'flv'
        else:
            ext = 'mp4'
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls(preferred[0], title, ext, size, output_dir=output_dir, merge=merge)
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
    assert re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/(\D|bangumi)/\D\D(\d+)', url)

    if re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/\D/\D\D(\d+)', url):
        html = get_content(url)
        title = r1(r'data-title="([^"]+)"', html)
        if match1(url, r'_(\d+)$'):  # current P
            title = title + " " + r1(r'active">([^<]*)', html)
        vid = r1('data-vid="(\d+)"', html)
        up = r1('data-name="([^"]+)"', html)
    # bangumi
    elif re.match("https?://[^\.]*\.*acfun\.[^\.]+/bangumi/ab(\d+)", url):
        html = get_content(url)
        title = match1(html, r'"title"\s*:\s*"([^"]+)"')
        if match1(url, r'_(\d+)$'):  # current P
            title = title + " " + r1(r'active">([^<]*)', html)
        vid = match1(html, r'videoId="(\d+)"')
        up = "acfun"
    else:
        raise NotImplemented

    assert title and vid
    title = unescape_html(title)
    title = escape_file_path(title)
    p_title = r1('active">([^<]+)', html)
    title = '%s (%s)' % (title, up)
    if p_title:
        title = '%s - %s' % (title, p_title)


    acfun_download_by_vid(vid, title,
                          output_dir=output_dir,
                          merge=merge,
                          info_only=info_only,
                          **kwargs)


site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
