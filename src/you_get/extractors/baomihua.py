#!/usr/bin/env python

__all__ = ['baomihua_download', 'baomihua_download_by_id']

from ..common import *

import urllib

def baomihua_headers(referer=None, cookie=None):
	# a reasonable UA
	ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
	headers = {'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': ua}
	if referer is not None:
		headers.update({'Referer': referer})
	if cookie is not None:
		headers.update({'Cookie': cookie})
	return headers
	
def baomihua_download_by_id(id, title=None, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html('http://play.baomihua.com/getvideourl.aspx?flvid=%s&devicetype=phone_app' % id)
    host = r1(r'host=([^&]*)', html)
    assert host
    type = r1(r'videofiletype=([^&]*)', html)
    assert type
    vid = r1(r'&stream_name=([^&]*)', html)
    assert vid
    dir_str = r1(r'&dir=([^&]*)', html).strip()
    url = "http://%s/%s/%s.%s" % (host, dir_str, vid, type)
    _, ext, size = url_info(url, headers=baomihua_headers())
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge, headers=baomihua_headers())

def baomihua_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    title = r1(r'<title>(.*)</title>', html)
    assert title
    id = r1(r'flvid\s*=\s*(\d+)', html)
    assert id
    baomihua_download_by_id(id, title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "baomihua.com"
download = baomihua_download
download_playlist = playlist_not_supported('baomihua')
