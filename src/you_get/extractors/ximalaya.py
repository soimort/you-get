#!/usr/bin/env python

__all__ = ['ximalaya_download_playlist', 'ximalaya_download', 'ximalaya_download_by_id']

from ..common import *

import json
import re

stream_types = [
        {'itag': '1', 'container': 'm4a', 'bitrate': 'default'},
        {'itag': '2', 'container': 'm4a', 'bitrate': '32'},
        {'itag': '3', 'container': 'm4a', 'bitrate': '64'}
        ]

def ximalaya_download_by_id(id, title = None, output_dir = '.', info_only = False, stream_id = None):
    BASE_URL = 'http://www.ximalaya.com/tracks/'
    json_url = BASE_URL + id + '.json'
    json_data = json.loads(get_content(json_url, headers=fake_headers))
    if 'res' in json_data:
        if json_data['res'] == False:
            raise ValueError('Server reported id %s is invalid' % id)
    if 'is_paid' in json_data and json_data['is_paid']:
        if 'is_free' in json_data and not json_data['is_free']:
            raise ValueError('%s is paid item' % id)
    if (not title) and 'title' in json_data:
        title = json_data['title']
#no size data in the json. should it be calculated?
    size = 0
    url = json_data['play_path_64']
    if stream_id:
        if stream_id == '1':
            url = json_data['play_path_32']
        elif stream_id == '0':
            url = json_data['play_path']
    logging.debug('ximalaya_download_by_id: %s' % url)
    ext = 'm4a' 
    urls = [url]
    print('Site:        %s' % site_info)
    print('title:       %s' % title)
    if info_only:
        if stream_id:
            print_stream_info(stream_id)
        else:
            for item in range(0, len(stream_types)):
                print_stream_info(item)
    if not info_only:
        print('Type:        MPEG-4 audio m4a')
        print('Size:        N/A')
        download_urls(urls, title, ext, size, output_dir = output_dir, merge = False)

def ximalaya_download(url, output_dir = '.', info_only = False, stream_id = None, **kwargs):
    if re.match(r'http://www\.ximalaya\.com/(\d+)/sound/(\d+)', url):
        id = match1(url, r'http://www\.ximalaya\.com/\d+/sound/(\d+)')
    else:
        raise NotImplementedError(url)
    ximalaya_download_by_id(id, output_dir = output_dir, info_only = info_only, stream_id = stream_id)

def ximalaya_download_page(playlist_url, output_dir = '.', info_only = False, stream_id = None, **kwargs):
    if re.match(r'http://www\.ximalaya\.com/(\d+)/album/(\d+)', playlist_url):
        page_content = get_content(playlist_url)
        pattern = re.compile(r'<li sound_id="(\d+)"')
        ids = pattern.findall(page_content)
        for id in ids:
            try:
                ximalaya_download_by_id(id, output_dir=output_dir, info_only=info_only, stream_id=stream_id)
            except(ValueError):
                print("something wrong with %s, perhaps paid item?" % id)
    else:
        raise NotImplementedError(playlist_url)
    
def ximalaya_download_playlist(url, output_dir='.', info_only=False, stream_id=None, **kwargs):
    match_result = re.match(r'http://www\.ximalaya\.com/(\d+)/album/(\d+)', url)
    if not match_result:
        raise NotImplementedError(url)
    pages = []
    page_content = get_content(url)
    if page_content.find('<div class="pagingBar_wrapper"') == -1:
        pages.append(url)
    else:
        base_url = 'http://www.ximalaya.com/' + match_result.group(1) + '/album/' + match_result.group(2)
        html_str = '<a href=(\'|")\/' + match_result.group(1) + '\/album\/' + match_result.group(2) + '\?page='
        count = len(re.findall(html_str, page_content))
        for page_num in range(count):
            pages.append(base_url + '?page=' +str(page_num+1))
            print(pages[-1])
    for page in pages:
        ximalaya_download_page(page, output_dir=output_dir, info_only=info_only, stream_id=stream_id)
def print_stream_info(stream_id):
    print('    - itag:        %s' % stream_id)
    print('      container:   %s' % 'm4a')
    print('      bitrate:     %s' % stream_types[int(stream_id)]['bitrate'])
    print('      size:        %s' % 'N/A')
    print('    # download-with: you-get --itag=%s [URL]' % stream_id)

site_info = 'ximalaya.com'
download = ximalaya_download
download_playlist = ximalaya_download_playlist 
