# coding=utf-8

import json
import re
from urllib import parse
from ..common import *

__all__ = ['douyin_download_by_url']

def douyin_download_by_url(url, **kwargs):
    # if short link, get the real url
    if 'v.douyin.com' in url:
        url = get_location(url)
    aweme_id = match1(url, r'/(\d+)/?')
    # get video info
    video_info_api = 'https://www.douyin.com/video/{}?previous_page=app_code_link'
    url = video_info_api.format(aweme_id)
    page_content = get_content(url, headers=fake_headers)
    json_data = re.findall(r'(?<=<script id=\"RENDER_DATA\" type=\"application\/json\">)(.*?)(?=<\/script>)', page_content)
    try:
        video_info = json.loads(parse.unquote(json_data[0]))
    except:
        log.wtf('[Error] Please specify a cookie file or cookie file need to be refresh.')
    
    data = None
    for _, v in video_info.items():
        if isinstance(v, str):
            continue
        if 'awemeId' in v:
            data = v['aweme']
    data = data['detail']

    # get video id and title
    title = data['desc']

    # get video play url (the highest rate) 
    rate = 0
    url = ''
    for item in data['video']['bitRateList']:
        if item['bitRate'] > rate:
            rate = item['bitRate']
            url = item['playApi']
    video_url = "https:" + url
    video_format = 'mp4'
    size = url_size(video_url, faker=True)
    print_info(
        site_info='douyin.com', title=title,
        type=video_format, size=size
    )
    if not kwargs['info_only']:
        download_urls(
            urls=[video_url], title=title, ext=video_format, total_size=size,
            faker=True,
            **kwargs
        )


download = douyin_download_by_url
download_playlist = playlist_not_supported('douyin')
