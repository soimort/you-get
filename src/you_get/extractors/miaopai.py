#!/usr/bin/env python

__all__ = ['miaopai_download']

import string
import random
from ..common import *
import urllib.error
import urllib.parse
from ..util import fs

fake_headers_mobile = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
}

def miaopai_download_by_fid(fid, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Source: Android mobile'''
    page_url = 'http://video.weibo.com/show?fid=' + fid + '&type=mp4'

    mobile_page = get_content(page_url, headers=fake_headers_mobile)
    url = match1(mobile_page, r'<video id=.*?src=[\'"](.*?)[\'"]\W')
    if url is None:
        wb_mp = re.search(r'<script src=([\'"])(.+?wb_mp\.js)\1>', mobile_page).group(2)
        return miaopai_download_by_wbmp(wb_mp, fid, output_dir=output_dir, merge=merge,
                                        info_only=info_only, total_size=None, **kwargs)
    title = match1(mobile_page, r'<title>((.|\n)+?)</title>')
    if not title:
        title = fid
    title = title.replace('\n', '_')
    ext, size = 'mp4', url_info(url)[2]
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)


def miaopai_download_by_wbmp(wbmp_url, fid, info_only=False, **kwargs):
    headers = {}
    headers.update(fake_headers_mobile)
    headers['Host'] = 'imgaliyuncdn.miaopai.com'
    wbmp = get_content(wbmp_url, headers=headers)
    appid = re.search(r'appid:\s*?([^,]+?),', wbmp).group(1)
    jsonp = re.search(r'jsonp:\s*?([\'"])(\w+?)\1', wbmp).group(2)
    population = [i for i in string.ascii_lowercase] + [i for i in string.digits]
    info_url = '{}?{}'.format('http://p.weibo.com/aj_media/info', parse.urlencode({
        'appid': appid.strip(),
        'fid': fid,
        jsonp.strip(): '_jsonp' + ''.join(random.sample(population, 11))
    }))
    headers['Host'] = 'p.weibo.com'
    jsonp_text = get_content(info_url, headers=headers)
    jsonp_dict = json.loads(match1(jsonp_text, r'\(({.+})\)'))
    if jsonp_dict['code'] != 200:
        log.wtf('[Failed] "%s"' % jsonp_dict['msg'])
    video_url = jsonp_dict['data']['meta_data'][0]['play_urls']['l']
    title = jsonp_dict['data']['description']
    title = title.replace('\n', '_')
    ext = 'mp4'
    headers['Host'] = 'f.us.sinaimg.cn'
    print_info(site_info, title, ext, url_info(video_url, headers=headers)[2])
    if not info_only:
        download_urls([video_url], fs.legitimize(title), ext, headers=headers, **kwargs)


def miaopai_download_direct(url, info_only, **kwargs):
    mobile_page = get_content(url, headers=fake_headers_mobile)
    try:
        title = re.search(r'([\'"])title\1:\s*([\'"])(.+?)\2,', mobile_page).group(3)
    except:
        title = re.search(r'([\'"])status_title\1:\s*([\'"])(.+?)\2,', mobile_page).group(3)
    title = title.replace('\n', '_')
    stream_url = re.search(r'([\'"])stream_url\1:\s*([\'"])(.+?)\2,', mobile_page).group(3)
    ext = 'mp4'
    print_info(site_info, title, ext, url_info(stream_url, headers=fake_headers_mobile)[2])
    if not info_only:
        download_urls([stream_url], fs.legitimize(title), ext, total_size=None, headers=fake_headers_mobile, **kwargs)


# ----------------------------------------------------------------------
def miaopai_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if match1(url, r'weibo\.com/tv/v/(\w+)'):
        return miaopai_download_direct(url, info_only=info_only, output_dir=output_dir, merge=merge, **kwargs)

    if re.match(r'^http[s]://.*\.weibo\.com/\d+/.+', url):
        return miaopai_download_direct(url, info_only=info_only, output_dir=output_dir, merge=merge, **kwargs)

    fid = match1(url, r'\?fid=(\d{4}:\w+)')
    if fid is not None:
        miaopai_download_by_fid(fid, output_dir, merge, info_only)
    elif '/p/230444' in url:
        fid = match1(url, r'/p/230444(\w+)')
        miaopai_download_by_fid('1034:'+fid, output_dir, merge, info_only)
    else:
        mobile_page = get_content(url, headers = fake_headers_mobile)
        hit = re.search(r'"page_url"\s*:\s*"([^"]+)"', mobile_page)
        if not hit:
            raise Exception('Unknown pattern')
        else:
            escaped_url = hit.group(1)
            miaopai_download(urllib.parse.unquote(escaped_url), output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)


site_info = "miaopai"
download = miaopai_download
download_playlist = playlist_not_supported('miaopai')
