#!/usr/bin/env python

__all__ = ['sohu_download']

from ..common import *

import json
import time
from random import random
from url.parse import urlparse
#http://115.25.217.132/?prot=9&prod=flash&pt=1&
#file=/v/Sample1/BackUp_Sample1/svc/20150604/1663504_2406534_v_H_231452_18500/1663504_2406534_v_H_231452_18500_001.mp4
#&new=/248/222/JwoalHHmSNWLsCVDEPqgTD.mp4
#&key=3q6dEeDbCZwpf-kydU-7TH0YDP5UxFdU&vid=2406534&tvid=1663504&uid=13796019242829873083&sz=1583_434&md=WG4FExsQg2SW3C8BylUDISibt+AaBtYlyoHEkA==179&t=0.928698823787272

def real_url(host,vid,tvid,new,clipURL,ck):
    url = 'http://'+host+'/?prot=9&prod=flash&pt=1&file='+clipURL+'&new='+new +'&key='+ ck+'&vid='+str(vid)+'&uid='+str(int(time.time()*1000))+'&t='+str(random())
    return json.loads(get_html(url))['url']

def sohu_download(url, output_dir = '.', merge = True, info_only = False, extractor_proxy=None):
    if re.match(r'http://share.vrs.sohu.com', url):
        vid = r1('id=(\d+)', url)
    else:
        html = get_html(url)
        vid = r1(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', html)
    assert vid

    if re.match(r'http://tv.sohu.com/', url):
        if extractor_proxy:
            set_proxy(tuple(extractor_proxy.split(":")))
        data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
        for qtyp in ["oriVid","superVid","highVid" ,"norVid","relativeId"]:
            hqvid = data['data'][qtyp]
            if hqvid != 0 and hqvid != vid :
                data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid))
                break
        if extractor_proxy:
            unset_proxy()
        host = data['allot']
        prot = data['prot']
        urls = []
        data = data['data']
        title = data['tvName']
        tvid = data['tvid']
        size = sum(data['clipsBytes'])
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new,clip,ck, in zip(data['su'],data['clipsURL']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host,hqvid,tvid,new,clipURL,ck))
        # assert data['clipsURL'][0].endswith('.mp4')

    else:
        data = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % vid))
        host = data['allot']
        prot = data['prot']
        urls = []
        data = data['data']
        title = data['tvName']
        tvid = data['tvid']
        size = sum(data['clipsBytes'])
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new,clip,ck, in zip(data['su'],data['clipsURL']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host,hqvid,tvid,new,clipURL,ck))

    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, output_dir, refer = url, merge = merge)

site_info = "Sohu.com"
download = sohu_download
download_playlist = playlist_not_supported('sohu')
