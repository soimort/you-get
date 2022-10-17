# coding=utf-8

import json

from ..common import (
    url_size,
    print_info,
    get_content,
    fake_headers,
    download_urls,
    playlist_not_supported,
    match1,
    get_location,
)

__all__ = ['douyin_download_by_url']


def get_value(source: dict, path):
    try:
        value = source
        for key in path:
            if type(key) is str:
                if key in value.keys():
                    value = value[key]
                else:
                    value = None
                    break
            elif type(key) is int:
                if len(value) != 0:
                    value = value[key]
                else:
                    value = None
                    break
    except:
        value = None
    return value


def douyin_download_by_url(url, **kwargs):
    # if short link, get the real url
    if 'v.douyin.com' in url:
        url = get_location(url)
    aweme_id = match1(url, r'/(\d+)/?')
    # get video info
    video_info_api = 'https://www.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'
    url = video_info_api.format(aweme_id)
    page_content = get_content(url, headers=fake_headers)
    video_info = json.loads(page_content)

    # get video id and title
    video_id = get_value(video_info, ['item_list', 0, 'video', 'vid'])
    title = get_value(video_info, ['item_list', 0, 'desc'])

    # get video play url
    video_url = "https://aweme.snssdk.com/aweme/v1/play/?ratio=720p&line=0&video_id={}".format(video_id)
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
