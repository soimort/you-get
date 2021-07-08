# coding=utf-8

import re
from urllib.parse import unquote

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
    # The easiest way to get the title is, obviously, from <title>
    title = re.findall(r'<title.*>(.*)</title>', page_content)[0].strip()
    # Remove the site name from title
    site_name = ' - 抖音'
    if title.endswith(site_name):
        title = title[:-len(site_name)]
    video_format = 'mp4'
    # The video url is url escaped, as of today, there are 4 working CDN video
    # urls for the same video, I chose the shortest one.
    cdn_pattern = r'(www\.douyin\.com%2Faweme.*PackSourceEnum_AWEME_DETAIL)'
    video_url = 'http://' + unquote(re.findall(cdn_pattern, page_content)[0])
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
