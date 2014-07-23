#!/usr/bin/env python

__all__ = ['facebook_download']

from ..common import *

def facebook_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    
    title = r1(r'<title id="pageTitle">(.+) \| Facebook</title>', html)
    
    for fmt in ["hd_src", "sd_src"]:
        src= re.sub(r'\\/', r'/', r1(r'"' + fmt + '":"([^"]*)"', parse.unquote(unicodize(r1(r'\["params","([^"]*)"\]', html)))))
        if src:
            break
    
    type, ext, size = url_info(src)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([src], title, ext, size, output_dir, merge = merge)

site_info = "Facebook.com"
download = facebook_download
download_playlist = playlist_not_supported('facebook')
