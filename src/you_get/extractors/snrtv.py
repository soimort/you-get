#!/usr/bin/env python

__all__ = ['snrtv_download']

from ..common import *
import lxml.etree



def snrtv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    '''
    Two page formats have been temporarily discovered
    http://www.snrtv.com/content/2018-07/06/content_15881533.htm
    http://www.snrtv.com/content/2018-02/09/content_15665751.htm
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    html = get_html(url,faker=True)
    title = r1('<title>([.\s\S]*?)</title>', html)
    title = title.replace(u'- 陕西网络广播电视台', '').replace('- Discover Shaanxi','').replace('- snrtv.com','')
    title = title.strip()
    if 'Discover Shaanxi' in html:
        html = lxml.etree.HTML(html)
        json_url = html.xpath('//div[@id="play_url"]/text()')
        if not json_url:
            return None
        json_url = json_url[0]
        json_str = get_html(json_url,faker=True)
        json_str = r1('({.*})', json_str)
        json_str = json.loads(json_str)
        m3u8_url = parse.unquote(json_str['m3u8'])
        urls = general_m3u8_extractor(m3u8_url,headers=headers)
        print_info(site_info, title, 'm3u8', 0)
        if not info_only:
            download_urls(urls, title, 'ts', 0, output_dir=output_dir,headers=headers, merge=merge, **kwargs)
    else:
        real_url = r1(r'videos\s*:\s*\[{url\s*:\s*"(http.*?)"\s*,\s*delay\s*:\d+\s*}\s*\]', html)
        type, ext, size = url_info(real_url,faker=True)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([real_url], title, ext, size, output_dir=output_dir, faker=True, headers=headers,merge=merge, **kwargs)

site_info = "snrtv.com"
download = snrtv_download
download_playlist = playlist_not_supported('snrtv')