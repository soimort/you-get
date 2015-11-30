#!/usr/bin/env python

__all__ = ['vidto_download']

from ..common import *
import pdb
import time


def vidto_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    params = {}
    r = re.findall(
        r'type="(?:hidden|submit)?"(?:.*?)name="(.+?)"\s* value="?(.+?)">', html)
    for name, value in r:
        params[name] = value
    data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url)
    print("Please wait for 6 seconds...")
    time.sleep(6)
    print("Starting")
    new_html = request.urlopen(req, data).read().decode('utf-8', 'replace')
    new_stff = re.search('lnk_download" href="(.*?)">', new_html)
    if(new_stff):
        url = new_stff.group(1)
        title = params['fname']
        type = ""
        ext = ""
        a, b, size = url_info(url)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir, merge=merge)
    else:
        print("cannot find link, please review")
        pdb.set_trace()


site_info = "vidto.me"
download = vidto_download
download_playlist = playlist_not_supported('vidto')
