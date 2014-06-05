#!/usr/bin/env python

__all__ = ['sohu_download']

from ..common import *

import json

def real_url(host, prot, file, new):
    
    #http://211.162.61.44/sohu/s26h23eab6/10/|377|115.174.81.252|isvS4ypzVNTehZucPYiuvSofPLJKZjjRfj-89w..|1|0|13|1803|1
    #http://220.181.61.212/?prot=2&file=/tv/HUGE/BackUp/hadoop/20140129/1134771_1575912_tv_S_030057_3101/1134771_1575912_tv_S_030057_3101_006.mp4&new=/95/134/sPDUFfcxumz9E19hrO5kF1.mp4&idc=377&key=P8F1ZUA9aCmlVvSwtSGLuf95W_fuRY69&vid=1575912&uid=14016791428538333287&sz=1663_538&md=exxLvREv9OqzTmsj6bmTAFSZZKl6wBx6OgUYqQ==206&t=0.7982267350889742
    i=0
    url = 'http://%s/?prot=%s&file=%s&new=%s' % (host, prot, file, new)
    while i<=5:
        try:
            start, idc, host2, key = get_html(url).split('|')[:4]
            realurl='%s%s?key=%s' % (start[:-1], new, key)
            response1=request.urlopen(realurl)
            return realurl
        except:
            url='http://%s/?prot=%s&file=%s&new=%s&idc=%s' % (host, prot, file, new,idc)
            #print(host)
            #print(url)
            start, idc, host2, key = get_html(url).split('|')[:4]
            i=i+1

def sohu_download(url, output_dir = '.', merge = True, info_only = False):
    if re.match(r'http://share.vrs.sohu.com', url):
        vid = r1('id=(\d+)', url)
    else:
        html = get_html(url)
        vid = r1(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', html)
    assert vid

    # Open Sogou proxy if required
    if get_sogou_proxy() is not None:
        server = sogou_proxy_server(get_sogou_proxy(), ostream=open(os.devnull, 'w'))
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        set_proxy(server.server_address)

    if re.match(r'http://tv.sohu.com/', url):
        data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
        for qtyp in ["oriVid","superVid","highVid" ,"norVid","relativeId"]:
            hqvid = data['data'][qtyp]
            if hqvid != 0 and hqvid != vid :
                data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid))
                break
        host = data['allot']
        prot = data['prot']
        urls = []
        data = data['data']
        title = data['tvName']
        size = sum(data['clipsBytes'])
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for file, new in zip(data['clipsURL'], data['su']):
            urls.append(real_url(host, prot, file, new))
        assert data['clipsURL'][0].endswith('.mp4')

    else:
        data = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % vid))
        host = data['allot']
        prot = data['prot']
        urls = []
        data = data['data']
        title = data['tvName']
        size = sum([int(clipsBytes) for clipsBytes in data['clipsBytes']])
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for file, new in zip(data['clipsURL'], data['su']):
            urls.append(real_url(host, prot, file, new))
        assert data['clipsURL'][0].endswith('.mp4')

    # Close Sogou proxy if required
    if get_sogou_proxy() is not None:
        server.shutdown()
        unset_proxy()

    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, output_dir, refer = url, merge = merge)

site_info = "Sohu.com"
download = sohu_download
download_playlist = playlist_not_supported('sohu')
