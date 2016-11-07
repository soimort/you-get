#!/usr/bin/env python

__all__ = ['vk_download']

from ..common import *


def get_video_info(url):
    video_page = get_content(url)
    title = r1(r'<div class="vv_summary">(.[^>]+?)</div', video_page)
    sources = re.findall(r'<source src=\"(.[^>]+?)"', video_page)

    for quality in ['.1080.', '.720.', '.480.', '.360.', '.240.']:
        for source in sources:
            if source.find(quality) != -1:
                url = source
                break
    assert url
    type, ext, size = url_info(url)
    print_info(site_info, title, type, size)

    return url, title, ext, size


def get_image_info(url):
    image_page = get_content(url)
    # used for title - vk page owner
    page_of = re.findall(r'Sender:</dt><dd><a href=.*>(.[^>]+?)</a', image_page)
    # used for title - date when photo was uploaded
    photo_date = re.findall(r'<span class="item_date">(.[^>]+?)</span', image_page)

    title = (' ').join(page_of + photo_date)
    image_link = r1(r'href="([^"]+)" class=\"mva_item\" target="_blank">Download full size', image_page)
    type, ext, size = url_info(image_link)
    print_info(site_info, title, type, size)

    return image_link, title, ext, size


def vk_download(url, output_dir='.', stream_type=None, merge=True, info_only=False, **kwargs):
    link = None
    if re.match(r'(.+)z\=video(.+)', url):
        link, title, ext, size = get_video_info(url)
    elif re.match(r'(.+)vk\.com\/photo(.+)', url):
        link, title, ext, size = get_image_info(url)
    else:
        raise NotImplementedError('Nothing to download here')

    if not info_only and link is not None:
        download_urls([link], title, ext, size, output_dir, merge=merge)


site_info = "VK.com"
download = vk_download
download_playlist = playlist_not_supported('vk')
