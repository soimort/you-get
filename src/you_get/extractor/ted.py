#!/usr/bin/env python

__all__ = ['ted_download']

from ..common import *

def ted_download(url, output_dir = '.', merge = True, info_only = False):
    page = get_html(url).split("\n")
    for line in page:
        if line.find("<title>") > -1:
            title = line.replace("<title>", "").replace("</title>", "").replace("\t", "")
            title = title[:title.find(' | ')]
        if line.find("no-flash-video-download") > -1:
            url = line.replace('<a id="no-flash-video-download" href="', "").replace(" ", "").replace("\t", "").replace(".mp4", "-480p.mp4")
            url = url[:url.find('"')]
            type, ext, size = url_info(url)
            print_info(site_info, title, type, size)
            if not info_only:
                download_urls([url], title, ext, size, output_dir, merge=merge)
            break

site_info = "TED.com"
download = ted_download
download_playlist = playlist_not_supported('ted')
