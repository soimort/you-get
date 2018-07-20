#!/usr/bin/env python

__all__ = ['miaopai_download']

from ..common import *
import urllib.error
import urllib.parse

fake_headers_mobile = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
}

def miaopai_download_by_fid(fid, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Source: Android mobile'''
    page_url = 'http://video.weibo.com/show?fid=' + fid + '&type=mp4'

    mobile_page = get_content(page_url, headers=fake_headers_mobile)
    url = match1(mobile_page, r'<video id=.*?src=[\'"](.*?)[\'"]\W')
    title = match1(mobile_page, r'<title>((.|\n)+?)</title>')
    if not title:
        title = fid
    title = title.replace('\n', '_')
    ext, size = 'mp4', url_info(url)[2]
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def miaopai_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    fid = match1(url, r'\?fid=(\d{4}:\w+)')
    if fid is not None:
        miaopai_download_by_fid(fid, output_dir, merge, info_only)
    elif '/p/230444' in url:
        fid = match1(url, r'/p/230444(\w+)')
        miaopai_download_by_fid('1034:'+fid, output_dir, merge, info_only)
    else:
        mobile_page = get_content(url, headers = fake_headers_mobile)
        hit = re.search(r'"page_url"\s*:\s*"([^"]+)"', mobile_page)
        if not hit:
            raise Exception('Unknown pattern')
        else:
            escaped_url = hit.group(1)
            miaopai_download(urllib.parse.unquote(escaped_url), output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

site_info = "miaopai"
download = miaopai_download
download_playlist = playlist_not_supported('miaopai')
