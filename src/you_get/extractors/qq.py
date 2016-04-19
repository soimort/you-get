#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *

def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
    api = "http://h5vv.video.qq.com/getinfo?otype=json&platform=10901&vid=%s" % vid
    content = get_html(api)
    output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
    url = output_json['vl']['vi'][0]['ul']['ui'][0]['url']
    fvkey = output_json['vl']['vi'][0]['fvkey']
    url = '%s/%s.mp4?vkey=%s' % ( url, vid, fvkey )
    _, ext, size = url_info(url, faker=True)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if 'v.qq.com/page' in url:
        # for URLs like this:
        # http://v.qq.com/page/k/9/7/k0194pwgw97.html
        # it will redirect.
        vid = match1(url, r'\b(\w+).html')
        title = vid
    elif 'kuaibao.qq.com' in url:
        content = get_html(url)
        vid = match1(content, r'vid\s*=\s*"\s*([^"]+)"')
        title = match1(content, r'title">([^"]+)</p>').strip()
    elif 'iframe/player.html' in url:
        vid = match1(url, r'\bvid=(\w+)')
        # for embedded URLs; don't know what the title is
        title = vid
    else:
        content = get_html(url)
        vid = match1(content, r'vid\s*:\s*"\s*([^"]+)"')
        title = match1(content, r'title\s*:\s*"\s*([^"]+)"')
        # try to get the right title for URLs like this:
        # http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5
        title = matchall(content, [r'title\s*:\s*"\s*([^"]+)"'])[-1]

    qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
