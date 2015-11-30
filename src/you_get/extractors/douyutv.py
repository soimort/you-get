#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
import json
import hashlib
import time

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    room_id = url[url.rfind('/')+1:]
    #Thanks to @yan12125 for providing decoding method!!
    suffix = 'room/%s?aid=android&client_sys=android&time=%d' % (room_id, int(time.time()))
    sign = hashlib.md5((suffix + '1231').encode('ascii')).hexdigest()
    json_request_url = "http://www.douyutv.com/api/v1/%s&auth=%s" % (suffix, sign)
    content = get_html(json_request_url)
    data = json.loads(content)['data']
    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)
    title = data.get('room_name')
    show_status = data.get('show_status')
    if show_status is not "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % server_status)
    real_url = data.get('rtmp_url')+'/'+data.get('rtmp_live')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "douyutv.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyutv')
