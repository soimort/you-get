#!/usr/bin/env python

__all__ = ['youtube_download', 'youtube_download_by_id']

from ..common import *

def youtube_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    html = request.urlopen('http://www.youtube.com/watch?v=' + id).read().decode('utf-8')
    
    title = r1(r'"title": "([^"]+)"', html)
    title = unicodize(title)
    title = parse.unquote(title)
    title = escape_file_path(title)
    
    url = r1(r'crossdomain.xml"\);yt.preload.start\("([^"]+)"\)', html)
    url = unicodize(url)
    url = re.sub(r'\\/', '/', url)
    url = re.sub(r'generate_204', 'videoplayback', url)
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def youtube_download(url, output_dir = '.', merge = True, info_only = False):
    id = parse.parse_qs(parse.urlparse(url).query)['v'][0]
    assert id
    
    youtube_download_by_id(id, None, output_dir, merge = merge, info_only = info_only)

site_info = "YouTube.com"
download = youtube_download
download_playlist = playlist_not_supported('youtube')
