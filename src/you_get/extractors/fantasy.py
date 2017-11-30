#!/usr/bin/env python

__all__ = ['fantasy_download']

from ..common import *
import json
import random
from urllib.parse import urlparse, parse_qs


def fantasy_download_by_id_channelId(id = 0, channelId = 0, output_dir = '.', merge = True, info_only = False,
                                     **kwargs):
    api_url = 'http://www.fantasy.tv/tv/playDetails.action?' \
              'myChannelId=1&id={id}&channelId={channelId}&t={t}'.format(id = id,
                                                                         channelId = channelId,
                                                                         t = str(random.random())
                                                                         )
    html = get_content(api_url)
    html = json.loads(html)

    if int(html['status']) != 100000:
        raise Exception('API error!')

    title = html['data']['tv']['title']

    video_url = html['data']['tv']['videoPath']
    headers = fake_headers.copy()
    headers['Referer'] = api_url
    type, ext, size = url_info(video_url, headers=headers)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, output_dir, merge = merge, headers = headers)


def fantasy_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if 'fantasy.tv' not in url:
        raise Exception('Wrong place!')

    q = parse_qs(urlparse(url).query)

    if 'tvId' not in q or 'channelId' not in q:
        raise Exception('No enough arguments!')

    tvId = q['tvId'][0]
    channelId = q['channelId'][0]

    fantasy_download_by_id_channelId(id = tvId, channelId = channelId, output_dir = output_dir, merge = merge,
                                     info_only = info_only, **kwargs)


site_info = "fantasy.tv"
download = fantasy_download
download_playlist = playlist_not_supported('fantasy.tv')
