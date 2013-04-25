#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *

def qq_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    url = 'http://vsrc.store.qq.com/%s.flv' % id
    
    _, _, size = url_info(url)
    
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls([url], title, 'flv', size, output_dir = output_dir, merge = merge)

def qq_download(url, output_dir = '.', merge = True, info_only = False):
    if re.match(r'http://v.qq.com/([^\?]+)\?vid', url):
        aid = r1(r'(.*)\.html', url)
        vid = r1(r'http://v.qq.com/[^\?]+\?vid=(\w+)', url)
        url = "%s/%s.html" % (aid, vid)
    
    if re.match(r'http://y.qq.com/([^\?]+)\?vid', url):
        vid = r1(r'http://y.qq.com/[^\?]+\?vid=(\w+)', url)
        
        url = "http://v.qq.com/page/%s.html" % vid
        
        r_url = r1(r'<meta http-equiv="refresh" content="0;url=([^"]*)', get_html(url))
        if r_url:
            aid = r1(r'(.*)\.html', r_url)
            url = "%s/%s.html" % (aid, vid)
    
    if re.match(r'http://static.video.qq.com/.*vid=', url):
        vid = r1(r'http://static.video.qq.com/.*vid=(\w+)', url)
        url = "http://v.qq.com/page/%s.html" % vid
    
    html = get_html(url)
    
    title = r1(r'title:"([^"]+)"', html)
    assert title
    title = unescape_html(title)
    title = escape_file_path(title)
    
    id = r1(r'vid:"([^"]+)"', html)
    
    qq_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
