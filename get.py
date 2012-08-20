#!/usr/bin/env python3

from common import *
import get_tudou
import get_yinyuetai
import get_youku
import get_youtube

def url_to_module(url):
    site = r1(r'http://([^/]+)/', url)
    assert site, 'invalid url: ' + url
    
    if site.endswith('.com.cn'):
        site = site[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', site)
    assert domain, 'unsupported url: ' + url
    
    k = r1(r'([^.]+)', domain)
    downloads = {
        'youtube': get_youtube,
        'youku': get_youku,
        'yinyuetai': get_yinyuetai,
        'tudou': get_tudou,
        #TODO:
        # 'acfun': get_acfun,
        # 'bilibili': get_bilibili,
        # 'kankanews': get_bilibili,
        # 'iask': get_iask,
        # 'sina': get_iask,
        # 'ku6': get_ku6,
        # 'pptv': get_pptv,
        # 'iqiyi': get_iqiyi,
        # 'sohu': get_sohu,
        # '56': get_w56,
        # 'cntv': get_cntv,
    }
    if k in downloads:
        return downloads[k]
    else:
        raise NotImplementedError(url)

def any_download(url, output_dir = '.', merge = True, info_only = False):
    m = url_to_module(url)
    m.download(url, output_dir = output_dir, merge = merge, info_only = info_only)

def any_download_playlist(url, output_dir = '.', merge = True, info_only = False):
    m = url_to_module(url)
    m.download_playlist(url, output_dir = output_dir, merge = merge, info_only = info_only)

if __name__ == '__main__':
    main('get.py', any_download, any_download_playlist)
