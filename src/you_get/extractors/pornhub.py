#!/usr/bin/env python

__all__ = ['pornhub_download']

import urllib.request, urllib.parse
from ..common import *


def pornhub_download(url, output_dir='.', merge=False, info_only=False, **kwargs):
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    viewkey = query["viewkey"]

    html = get_html('https://www.pornhub.com/embed/' + viewkey)

    title = re.findall(r'<title>(.*?)</title>', html)[0]
    p = re.compile("<script>(.*?)</script>", re.DOTALL)
    js = re.findall(p, html)
    jsf = js[0].replace('\n', '').replace('\t', '')
    comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    cdata = re.sub(comment, "", jsf)
    cs = cdata.replace(r'var ', '').split(";")

    param_dict = {}
    for c in cs:
        if c.find("=") != -1:
            ca = c.split("=", 1)
            param_dict[ca[0]] = ca[1].replace(r'" + "', '').strip(r'"')

    real_url = ""
    mp = []
    if "mp4480p" in param_dict:
        mp = param_dict["mp4480p"].split(r' + ')
    elif "mp4720p" in param_dict:
        mp = param_dict["mp4720p"].split(r' + ')
    elif "mp41080p" in param_dict:
        mp = param_dict["mp41080p"].split(r' + ')

    if len(mp) == 0:
        raise Exception('Resource not found!')

    for m in mp:
        real_url = real_url + param_dict[m]

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge=merge)


site_info = "pornhub.com"
download = pornhub_download
download_playlist = playlist_not_supported('pornhub')
