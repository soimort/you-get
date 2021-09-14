# coding=utf-8
import base64
import re

from ..common import (
    url_size,
    print_info,
    get_content,
    fake_headers,
    download_urls,
    playlist_not_supported,
)

__all__ = ['meipai_download_by_url']


def decode(content):
    def getHex(a):
        hex_1 = a[:4][::-1]
        str_1 = a[4:]
        return str_1, hex_1

    def getDec(a):
        b = str(int(a, 16))
        c = list(b[:2])
        d = list(b[2:])
        return c, d

    def substr(a, b):
        k = int(b[0])
        c = a[:k]
        d = a[k:k + int(b[1])]
        temp = a[int(b[0]):].replace(d, "")
        result = c + temp
        return result

    def getPos(a, b):
        b[0] = len(a) - int(b[0]) - int(b[1])
        return b

    str1, hex1 = getHex(content)
    pre, tail = getDec(hex1)
    d = substr(str1, pre)
    kk = substr(d, getPos(d, tail))
    return str(base64.b64decode(kk), "utf-8")


def meipai_download_by_url(url, **kwargs):
    # https://www.meipai.com/media/6843084314155964653
    page_content = get_content(url, headers=fake_headers)
    title = re.findall(r'<meta name=\"description\" content=\"(.*?)\" \/>', page_content)[0].strip()
    # Reference the "data-video" attribute in the <div id="detailvideo" /> tag,
    # Use the decode function to get the video source.
    video_url = "https:" + decode(re.findall(r'data-video=\"(.*?)\"', page_content)[0].strip())
    video_format = 'mp4'
    size = url_size(video_url, faker=True)
    print_info(
        site_info='meipai.com', title=title,
        type=video_format, size=size
    )
    if not kwargs['info_only']:
        download_urls(
            urls=[video_url], title=title, ext=video_format, total_size=size,
            faker=True,
            **kwargs
        )


download = meipai_download_by_url
download_playlist = playlist_not_supported('meipai')
