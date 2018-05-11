# coding=utf-8

import re
import json

from ..common import (
    url_size,
    print_info,
    get_content,
    fake_headers,
    download_urls,
    playlist_not_supported,
)


__all__ = ['douyin_download_by_url']


def douyin_download_by_url(url, **kwargs):
    page_content = get_content(url, headers=fake_headers)
    match_rule = re.compile(r'var data = \[(.*?)\];')
    video_info = json.loads(match_rule.findall(page_content)[0])
    video_url = video_info['video']['play_addr']['url_list'][0]
    # fix: https://www.douyin.com/share/video/6553248251821165832
    # if there is no title, use desc
    cha_list = video_info['cha_list']
    if cha_list:
        title = cha_list[0]['cha_name']
    else:
        title = video_info['desc']
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
