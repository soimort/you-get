#!/usr/bin/env python

__all__ = ['iqiyi_download']

from ..common import *

def iqiyi_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)

    tvid = r1(r'data-player-tvid="([^"]+)"', html)
    videoid = r1(r'data-player-videoid="([^"]+)"', html)
    assert tvid
    assert videoid

    info_url = 'http://cache.video.qiyi.com/vj/%s/%s/' % (tvid, videoid)
    info = get_html(info_url)
    raise NotImplementedError('iqiyi')

    from xml.dom.minidom import parseString
    doc = parseString(info_xml)
    title = doc.getElementsByTagName('title')[0].firstChild.nodeValue
    size = int(doc.getElementsByTagName('totalBytes')[0].firstChild.nodeValue)
    urls = [n.firstChild.nodeValue for n in doc.getElementsByTagName('file')]
    assert urls[0].endswith('.f4v'), urls[0]

    for i in range(len(urls)):
        temp_url = "http://data.video.qiyi.com/%s" % urls[i].split("/")[-1].split(".")[0] + ".ts"
        try:
            response = request.urlopen(temp_url)
        except request.HTTPError as e:
            key = r1(r'key=(.*)', e.geturl())
        assert key
        urls[i] += "?key=%s" % key

    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir = output_dir, merge = merge)

site_info = "iQIYI.com"
download = iqiyi_download
download_playlist = playlist_not_supported('iqiyi')
