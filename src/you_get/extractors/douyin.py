# coding=utf-8

import re
import json

from ..common import (
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['douyin_download_by_url']


def douyin_download_by_url(url, **kwargs):
    page_content = get_content(url)
    match_rule = re.compile(r'var data = \[(.*?)\];')
    video_info = json.loads(match_rule.findall(page_content)[0])
    video_url = video_info['video']['play_addr']['url_list'][0]
    title = video_info['cha_list'][0]['cha_name']
    video_format = 'mp4'
    size = url_size(video_url)
    print_info(
        site_info='douyin.com', title=title,
        type=video_format, size=size
    )
    if not kwargs['info_only']:
        download_urls(
            urls=[video_url], title=title, ext=video_format, total_size=size,
            **kwargs
        )


download = douyin_download_by_url
download_playlist = playlist_not_supported('douyin')
