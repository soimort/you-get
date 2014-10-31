#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
import re
import json

def douyutv_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    room_id_patt = r'"room_id":(\d{1,99}),'
    title_patt = r'<div class="headline clearfix">\s*<h1>([^<]{1,9999})</h1>\s*</div>'
    
    roomid = re.findall(room_id_patt,html)[0]
    title = unescape_html(re.findall(title_patt,html)[0])

    conf = get_html("http://www.douyutv.com/api/client/room/"+roomid)
    metadata = json.loads(conf)
    
    rtmp_live= metadata.get('data').get('rtmp_live')
    rtmp_url= metadata.get('data').get('rtmp_url')
    real_url = rtmp_url+'/'+rtmp_live

    type, _, _ = url_info(real_url)
    
    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "douyutv.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyutv')
