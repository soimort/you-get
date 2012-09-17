#!/usr/bin/env python

__all__ = ['youtube_download', 'youtube_download_by_id']

from ..common import *

def youtube_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    try:
        url = parse.parse_qs(parse.unquote(request.urlopen('http://www.youtube.com/get_video_info?&video_id=' + id).read().decode('utf-8')))['url_encoded_fmt_stream_map'][0][4:]
    except:
        html = request.urlopen('http://www.youtube.com/watch?v=' + id).read().decode('utf-8')
        url = parse.parse_qs(parse.unquote(html))['url_encoded_fmt_stream_map'][0][4:]
        if not url.startswith('http://'):
            codec = r1(r'yt.preload.start\("http:\\/\\/([^\\]+)\\/crossdomain.xml"\)', html)
            signature = r1(r'signature=([^\\]+)\\', html)
            urls = parse.parse_qs(parse.unquote(html))['url']
            for u in urls:
                if u.startswith('http://' + codec):
                    url = "%s&signature=%s" % (u, signature)
                    break
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def youtube_download(url, output_dir = '.', merge = True, info_only = False):
    id = parse.parse_qs(parse.urlparse(url).query)['v'][0]
    assert id
    try:
        title = parse.parse_qs(parse.unquote(request.urlopen('http://www.youtube.com/get_video_info?&video_id=' + id).read().decode('utf-8')))['title'][0]
    except:
        html = get_html(url, 'utf-8')
        title = r1(r'"title": "([^"]+)"', html)
        title = unicodize(title)
    assert title
    title = parse.unquote(title)
    title = escape_file_path(title)
    youtube_download_by_id(id, title, output_dir, merge = merge, info_only = info_only)

site_info = "YouTube.com"
download = youtube_download
download_playlist = playlist_not_supported('youtube')
