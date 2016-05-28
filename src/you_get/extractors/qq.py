#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *
from .qie import download as qieDownload
from urllib.parse import urlparse,parse_qs
def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
    api = "http://h5vv.video.qq.com/getinfo?otype=json&platform=10901&vid=%s" % vid
    content = get_html(api)
    output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
    url = output_json['vl']['vi'][0]['ul']['ui'][0]['url']
    fvkey = output_json['vl']['vi'][0]['fvkey']
    mp4 = output_json['vl']['vi'][0]['cl'].get('ci', None)
    if mp4:
        mp4 = mp4[0]['keyid'].replace('.10', '.p') + '.mp4'
    else:
        mp4 = output_json['vl']['vi'][0]['fn']
    url = '%s/%s?vkey=%s' % ( url, mp4, fvkey )
    _, ext, size = url_info(url, faker=True)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if 'live.qq.com' in url:
        qieDownload(url,output_dir=output_dir, merge=merge, info_only=info_only)
        return 

    #do redirect
    if 'v.qq.com/page' in url:
        # for URLs like this:
        # http://v.qq.com/page/k/9/7/k0194pwgw97.html
        content = get_html(url)
        url = match1(content,r'window\.location\.href="(.*?)"')
        
    if 'kuaibao.qq.com' in url:
        content = get_html(url)
        vid = match1(content, r'vid\s*=\s*"\s*([^"]+)"')
        title = match1(content, r'title">([^"]+)</p>')
        title = title.strip() if title else vid
    elif 'iframe/player.html' in url:
        vid = match1(url, r'\bvid=(\w+)')
        # for embedded URLs; don't know what the title is
        title = vid
    else:
        content = get_html(url)
        vid = parse_qs(urlparse(url).query).get('vid') #for links specified vid  like http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5 
        vid = vid[0] if vid else match1(content, r'vid\s*:\s*"\s*([^"]+)"') #general fallback
        title = match1(content,r'<a.*?id\s*=\s*"%s".*?title\s*=\s*"(.+?)".*?>'%vid)
        title = match1(content, r'title">([^"]+)</p>') if not title else title
        title = vid if not title else title #general fallback



    qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
