#!/usr/bin/env python

__all__ = ['google_download']

from ..common import *

import re

def google_download(url, output_dir = '.', merge = True, info_only = False):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe = ':/+%')
    
    service = url.split('/')[2].split('.')[0]
    
    if service == 'plus': # Google Plus
        
        if re.search(r'plus.google.com/photos/\d+/albums/\d+/\d+', url):
            oid = r1(r'plus.google.com/photos/(\d+)/albums/\d+/\d+', url)
            pid = r1(r'plus.google.com/photos/\d+/albums/\d+/(\d+)', url)
            
        elif re.search(r'plus.google.com/photos/\d+/albums/posts/\d+', url):
            oid = r1(r'plus.google.com/photos/(\d+)/albums/posts/\d+', url)
            pid = r1(r'plus.google.com/photos/\d+/albums/posts/(\d+)', url)
            
        else:
            html = get_html(url)
            oid = r1(r'"https://plus.google.com/photos/(\d+)/albums/\d+/\d+', html)
            pid = r1(r'"https://plus.google.com/photos/\d+/albums/\d+/(\d+)', html)
        
        url = "http://plus.google.com/photos/%s/albums/posts/%s?oid=%s&pid=%s" % (oid, pid, oid, pid)
        
        html = get_html(url)
        real_url = unicodize(r1(r'"(https://video.googleusercontent.com/[^"]*)",\d\]', html).replace('\/', '/'))
        
        title = r1(r"\"([^\"]+)\",\"%s\"" % pid, html)
        if title is None:
            response = request.urlopen(request.Request(real_url))
            if response.headers['content-disposition']:
                filename = parse.unquote(r1(r'filename="?(.+)"?', response.headers['content-disposition'])).split('.')
                title = ''.join(filename[:-1])
        
        type, ext, size = url_info(real_url)
        if ext is None:
            ext = 'mp4'
        
    elif service in ['docs', 'drive'] : # Google Docs
        
        html = get_html(url)
        
        title = r1(r'"title":"([^"]*)"', html) or r1(r'<meta itemprop="name" content="([^"]*)"', html)
        if len(title.split('.')) > 1:
            title = ".".join(title.split('.')[:-1])
        
        docid = r1(r'"docid":"([^"]*)"', html)
        
        request.install_opener(request.build_opener(request.HTTPCookieProcessor()))
        
        request.urlopen(request.Request("https://docs.google.com/uc?id=%s&export=download" % docid))
        real_url ="https://docs.google.com/uc?export=download&confirm=no_antivirus&id=%s" % docid
        
        type, ext, size = url_info(real_url)
        
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Google.com"
download = google_download
download_playlist = playlist_not_supported('google')
