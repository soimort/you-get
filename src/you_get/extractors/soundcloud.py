#!/usr/bin/env python

__all__ = ['sndcd_download']

from ..common import *
import re
import json
import urllib.error


def get_sndcd_apikey():
    home_page = get_content('https://soundcloud.com')
    js_url = re.findall(r'script crossorigin src="(.+?)"></script>', home_page)[-1]

    client_id = get_content(js_url)
    return re.search(r'client_id:"(.+?)"', client_id).group(1)


def get_resource_info(resource_url, client_id):
    cont = get_content(resource_url, decoded=True)

    x = re.escape('forEach(function(e){n(e)})}catch(e){}})},')
    x = re.search(r'' + x + r'(.*)\);</script>', cont)

    info = json.loads(x.group(1))[-1]['data'][0]

    info = info['tracks'] if info.get('track_count') else [info]

    ids = [i['id'] for i in info if i.get('comment_count') is None]
    ids = list(map(str, ids))
    ids_split = ['%2C'.join(ids[i:i+10]) for i in range(0, len(ids), 10)]
    api_url = 'https://api-v2.soundcloud.com/tracks?ids={ids}&client_id={client_id}&%5Bobject%20Object%5D=&app_version=1584348206&app_locale=en'

    res = []
    for ids in ids_split:
        uri = api_url.format(ids=ids, client_id=client_id)
        cont = get_content(uri, decoded=True)
        res += json.loads(cont)

    res = iter(res)
    info = [next(res) if i.get('comment_count') is None else i for i in info]

    return info


def sndcd_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    client_id = get_sndcd_apikey()

    r_info = get_resource_info(url, client_id)

    for info in r_info:
        title = info['title']
        metadata = info.get('publisher_metadata')

        transcodings = info['media']['transcodings']
        sq = [i for i in transcodings if i['quality'] == 'sq']
        hq = [i for i in transcodings if i['quality'] == 'hq']
        # source url
        surl = sq[0] if hq == [] else hq[0]
        surl = surl['url']

        uri = surl + '?client_id=' + client_id
        r = get_content(uri)
        surl = json.loads(r)['url']

        m3u8 = get_content(surl)
        # url list
        urll = re.findall(r'http.*?(?=\n)', m3u8)

        size = urls_size(urll)
        print_info(site_info, title, 'audio/mpeg', size)
        print(end='', flush=True)

        if not info_only:
            download_urls(urll, title=title, ext='mp3', total_size=size, output_dir=output_dir, merge=True)


site_info = "SoundCloud.com"
download = sndcd_download
download_playlist = sndcd_download
