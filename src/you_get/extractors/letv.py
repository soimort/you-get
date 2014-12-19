#!/usr/bin/env python

__all__ = ['letv_download', 'letvcloud_download', 'letvcloud_download_by_vu']

import json
import random
import xml
import xml.etree.ElementTree as ET
import base64, hashlib, urllib
import os
import sys
import inspect
import io
import bs4, requests
import time
import urllib.request
import urllib.parse


currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(os.path.dirname(currentDir))
se_parentDir = os.path.dirname(parentDir)
sys.path.append(parentDir)
sys.path.append(se_parentDir)

print(currentDir)
print(parentDir)

from ..common import *

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
OSTYPE = 'MacOS10.10.1'

def get_timestamp():
    tn = random.random()
    url = 'http://api.letv.com/time?tn={}'.format(tn)
    result = get_content(url)
    return json.loads(result)['stime']

def get_key(t):
    for s in range(0, 8):
        e = 1 & t
        t >>= 1
        e <<= 31
        t += e
    return t ^ 185025305

def video_info(vid):
    tn = get_timestamp()
    key = get_key(tn)
#old api reserve for future use or for example
    # url = 'http://api.letv.com/mms/out/video/play?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(vid, key)
    # print(url)
    # r = get_content(url, decoded=False)
    # print(r)
    # xml_obj = ET.fromstring(r)
    # info = json.loads(xml_obj.find("playurl").text)
    # title = info.get('title')
    # urls = info.get('dispatch')
    # for k in urls.keys():
    #     url = urls[k][0]
    #     break
    # url += '&termid=1&format=0&hwtype=un&ostype=Windows7&tag=letv&sign=letv&expect=1&pay=0&rateid={}'.format(k)
    # return url, title

    url="http://api.letv.com/mms/out/common/geturl?platid=3&splatid=301&playid=0&vtype=9,13,21,28&version=2.0&tss=no&vid={}&domain=www.letv.com&tkey={}".format(vid,key)
    r = get_content(url, decoded=False)
    info=json.loads(str(r,"utf-8"))
    size=0
    for i in info["data"][0]["infos"]: #0 means only one file not truncated.need to upgrade
        if int(i["gsize"])>size:
            size=int(i["gsize"])
            url=i["mainUrl"]

    url+="&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=Linux&tag=letv&sign=letv&expect=3&tn={}&pay=0&iscpn=f9051&rateid=1300".format(random.random())
    # url += '&termid=1&format=0&hwtype=un&ostype=Windows7&tag=letv&sign=letv&expect=1&pay=0&rateid=1000'   #{}'.format(k)
    r2=get_content(url,decoded=False)
    info2=json.loads(str(r2,"utf-8"))
    return info2["location"]

def letv_download_by_vid(vid,title, output_dir='.', merge=True, info_only=False):
    url= video_info(vid)
    _, _, size = url_info(url)
    ext = 'flv'
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def letvcloud_download_by_vu(vu, title=None, output_dir='.', merge=True, info_only=False):
    str2Hash = 'cfflashformatjsonran0.7214574650861323uu2d8c027396ver2.1vu' + vu + 'bie^#@(%27eib58'
    sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
    request_info = urllib.request.Request('http://api.letvcloud.com/gpc.php?&sign='+sign+'&cf=flash&vu='+vu+'&ver=2.1&ran=0.7214574650861323&qr=2&format=json&uu=2d8c027396')
    response = urllib.request.urlopen(request_info)
    data = response.read()
    info = json.loads(data.decode('utf-8'))
    type_available = []
    for i in info['data']['video_info']['media']:
        type_available.append({'video_url': info['data']['video_info']['media'][i]['play_url']['main_url'], 'video_quality': int(info['data']['video_info']['media'][i]['play_url']['vtype'])})
    urls = [base64.b64decode(sorted(type_available, key = lambda x:x['video_quality'])[-1]['video_url']).decode("utf-8")]
    size = urls_size(urls)
    ext = 'mp4'
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir=output_dir, merge=merge)

def letvcloud_download(url, output_dir='.', merge=True, info_only=False):
    for i in url.split('&'):
        if 'vu=' in i:
            vu = i[3:]
    if len(vu) == 0:
        raise ValueError('Cannot get vu!')
    title = "LETV-%s" % vu
    letvcloud_download_by_vu(vu, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

def letv_download(url, output_dir='.', merge=True, info_only=False):
    if re.match(r'http://yuntv.letv.com/', url):
        letvcloud_download(url, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        """
        html = get_content(url)
        #to get title
        if re.match(r'http://www.letv.com/ptv/vplay/(\d+).html', url):
            vid = match1(url, r'http://www.letv.com/ptv/vplay/(\d+).html')
        else:
            vid = match1(html, r'vid="(\d+)"')
        title = match1(html,r'name="irTitle" content="(.*?)"')

        letv_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

        """

        title, vid, nextvid = letv_get_vid2title(url)
        letv_download_by_vid_sub(vid, nextvid, title=title, output_dir=output_dir,
                                 merge=merge, info_only=info_only)


def to_dict(dict_str):
    class _dict(dict):
        def __getitem__(self, key):
            return key
    return eval(dict_str, _dict())


def ror(a, b):
    c = 0
    while c < b:
        a = (0x7fffffff & (a >> 1)) + (0x80000000 & (a << 31))
        c += 1
    return a


def get_tkey(tm=None):
    l2 = 773625421
    if not tm:
        tm = int(time.time())
    l3 = ror(tm, l2 % 13)
    l3 ^= l2
    l3 = ror(l3, l2 % 17)
    if l3 & 0x80000000:
        return l3 - 0x100000000
    return l3


def letv_get_vid2title(page_url):
    #browser = Browser()
    #browser.set_handle_robots(False)
    #browser.addheaders = [('User-Agent', USER_AGENT)]

    #resp = browser.open(page_url)
    #resp_body = resp.read()

    #request = urllib.request.Request(page_url)
    #request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0')
    #response = urllib.request.urlopen(request)
    #resp_body = response.read()

    """
    tree = html.fromstring(resp_body)
    for script in tree.xpath('/html/head/script'):
    """
    #print(resp_body)

    response = requests.get(page_url)
    tree = bs4.BeautifulSoup(response.text)
    for script in tree.select('head script'):
        match_info = []
        start = False
        if not script.text:
            continue
        for line in script.text.split('\n'):
            if not start:
                match = re.match('var\s+__INFO__\s?=(.+)', line)
                if match:
                    start = True
                    match_info.append(match.group(1))
            else:
                if line.startswith('var'):
                    start = False
                    break
                hp = line.find('://')
                p = line.rfind('//')
                if p != -1 and p != hp+1:
                    match_info.append(line[:p])
                else:
                    match_info.append(line)
        if match_info:
            break

    match_info = '\n'.join(match_info)
    match_info = to_dict(match_info)
    vid = match_info['video']['vid']
    nextvid = match_info['video']['nextvid']
    #print '%s' % match_info['video']['title']
    title = match_info['video']['title']

    return (title, vid, nextvid)


def letv_download_by_vid_sub(vid, nextvid, title, output_dir='.', merge=True, info_only=False):
    """
    browser = Browser()
    browser.set_handle_robots(False)
    browser.addheaders = [
        ('User-Agent', USER_AGENT),
        ('Referer', 'http://player.letvcdn.com/p/201411/14/10/newplayer/LetvPlayer.swf')
    ]
    """

    param_dict = {
        'id': vid,
        'platid': 1,
        'splatid': 101,
        'format': 1,
        'nextvid': nextvid,
        'tkey': get_tkey(),
        'domain': 'www.letv.com'
    }

    url = 'http://api.letv.com/mms/out/video/playJson?%s' % urllib.parse.urlencode(param_dict)

    #resp = browser.open(url)
    #resp_body = resp.read()

    #request = urllib.request.Request(url)
    #request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0')
    #request.add_header('Referer', 'http://player.letvcdn.com/p/201411/14/10/newplayer/LetvPlayer.swf')

    #response = urllib.request.urlopen(request)
    #resp_body = response.read()

    response = requests.get(url)
    resp_body = response.text
    resp_dict = json.loads(str(resp_body))

    assert resp_dict['statuscode'] == '1001'
    assert resp_dict['playstatus']['status'] == '1'

    playurls = resp_dict['playurl']['dispatch']
    domains = resp_dict['playurl']['domain']
    duration = int(resp_dict['playurl']['duration'])

    #print 'Avaliable Size:', ' '.join(playurls.keys())
    keys = ['1080p', '720p', '1300', '1000', '350']
    for key in keys:
        playurl = playurls.get(key)
        if playurl:
            break

    #print 'Select %s' % key
    assert playurl

    tn = random.random()
    url = domains[0] + playurl[0] + '&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=%s&tag=letv&sign=letv&expect=3&tn=%s&pay=0&rateid=%s' % (OSTYPE, tn, key)

    #resp = browser.open(url)
    #gslb_data = json.loads(resp.read())

    #request = urllib.request.Request(url)
    #response = urllib.request.urlopen(request)
    #gslb_data = json.loads(str(response.read()) )

    response = requests.get(url)
    gslb_data = json.loads(response.text)

#    import pprint
#    pprint.pprint(resp_dict)
#    pprint.pprint(gslb_data)
    play_url = gslb_data.get('location')

    """
    file_name_m3u8 = os.path.basename(urlparse.urlsplit(play_url).path)
    file_name = '%s.ts' % os.path.splitext(file_name_m3u8)[0]
    target_file = os.path.join(target_dir, file_name)


    """

    url= play_url
    size = 0
    ext = 'm3u8'
    print_info(site_info, title, ext, size)
    #print "###LETV:m3u8:%s" % url
    print("###LETV:m3u8{}".format(url))

    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)


site_info = "LeTV.com"
download = letv_download
download_playlist = playlist_not_supported('letv')



if __name__ == '__main__':
    #page_url = "http://www.letv.com/ptv/vplay/21371716.html"
    #page_url = "http://www.letv.com/ptv/vplay/21470739.html"
    #page_url = "http://www.letv.com/ptv/vplay/21470465.html"
    #page_url = "http://www.letv.com/ptv/vplay/21470448.html"
    #target_dir = "./"

    letv_download("http://www.letv.com/ptv/vplay/21470448.html", './', True, True)
    pass
