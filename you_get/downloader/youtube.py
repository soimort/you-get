#!/usr/bin/env python

__all__ = ['youtube_download', 'youtube_download_by_id']

from ..common import *

import json

def youtube_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    html = request.urlopen('http://www.youtube.com/watch?v=' + id).read().decode('utf-8')
    
    html = unescape_html(html)
    yt_player_config = json.loads(r1(r'yt.playerConfig = ([^\n]+);\n', html))
    title = yt_player_config['args']['title']
    title = unicodize(title)
    title = parse.unquote(title)
    title = escape_file_path(title)
    
    for itag in [
        '38',
        '46', '37',
        '102', '45', '22',
        '84',
        '120',
        '85',
        '44', '35',
        '101', '100', '43', '34', '82', '18',
        '6',
        '83', '5', '36',
        '17',
        '13',
    ]:
        fmt = r1(r'([^,\"]*itag=' + itag + "[^,\"]*)", html)
        if fmt:
            url = r1(r'url=([^\\]+)', fmt)
            url = unicodize(url)
            url = parse.unquote(url)
            sig = r1(r'sig=([^\\]+)', fmt)
            url = url + '&signature=' + sig
            break
    try:
        url
    except NameError:
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
