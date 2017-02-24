from ..common import *
import xml.etree.ElementTree as ET
import re
import sys

__all__ = ['spankbang_download']


def spankbang_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    #todo: add support for chosing streams of different quality (ie. -F | --format OPTION )
    video_url_pattern = r'http://spankbang.com/_{stream_id}/{stream_key}/title/{quality}'
    stream_types = [('q_super','1080p__mp4'),
                    ('q_high','720p__mp4'),
                    ('q_medium','480p__mp4'),
                    ('q_low','240p__mp4')]
    
    content = get_decoded_html(url, faker = True)
    stream_id = re.findall(r'stream_id.+?\'(.+)\'',content)[0]
    stream_key = re.findall(r'stream_key.+?\'(.+)\'',content)[0]
    for key, value in stream_types:
        if content.find(key) != -1:
            video_url = video_url_pattern.format(stream_id=stream_id, stream_key=stream_key, quality=value)
            break
    
        
    src = video_url
    title = url.split('/')[-1]
    _, ext, size = url_info(src, faker = True)
    print_info(site_info, title, ext, size)
    
    if not info_only:
        download_urls([src], title, ext, size, output_dir = output_dir, merge = merge, faker = True)
            
            
            
site_info = 'spankbang.com'
download = spankbang_download
download_playlist = playlist_not_supported('spankbang')
