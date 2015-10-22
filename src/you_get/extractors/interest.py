#!/usr/bin/env python

from ..common import *
from json import loads

def interest_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    #http://ch.interest.me/zhtv/VOD/View/114789
    #http://program.interest.me/zhtv/sonja/8/Vod/View/15794
    html = get_content(url)
    #get title
    title = match1(html, r'<meta property="og:title" content="([^"]*)"')
    title = title.split('&')[0].strip()
    info_url = match1(html, r'data: "(.+)",')
    play_info = loads(get_content(info_url))
    try:
        serverurl = play_info['data']['cdn']['serverurl']
    except KeyError:
        raise ValueError('Cannot_Get_Play_URL')
    except:
        raise ValueError('Cannot_Get_Play_URL')
    # I cannot find any example of "fileurl", so i just put it like this for now
    assert serverurl

    type, ext, size = 'mp4', 'mp4', 0

    print_info(site_info, title, type, size)
    if not info_only:
        download_rtmp_url(url=serverurl, title=title, ext=ext, output_dir=output_dir)

site_info = "interest.me"
download = interest_download
download_playlist = playlist_not_supported('interest')
