#!/usr/bin/env python
__all__ = ['kissanime_download']

from ..common import *
import json
import cfscrape
import base64



def kissanime_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content

    btitle = re.search(b'<title>(.*)</title>', html, flags=re.DOTALL).group(1)
    title = ' '.join(str.join(" ", re.search(' (.*)-', btitle.decode('UTF-8'), flags=re.DOTALL).group(1).strip('\t, \r, \n').splitlines()).split())

    selectQuality = re.search(b'<select id="selectQuality">.*</select>', html).group(0)
    options = re.findall(b'<option value="([^"]+)', selectQuality)
    if options:
        url = ""
        for val in options:
            url += "\n"+base64.b64decode(val).decode("UTF-8")
    url_list = [y for y in (x.strip() for x in url.splitlines()) if y]
    url = url_list[0]
    type, ext, size = url_info(url, faker=True)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "KissAnime.com"
download = kissanime_download
download_playlist = playlist_not_supported('kissanime')
