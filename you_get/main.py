#!/usr/bin/env python

__all__ = ['main', 'any_download', 'any_download_playlist']

from .downloader import *
from .common import *

def url_to_module(url):
    site = r1(r'http://([^/]+)/', url)
    assert site, 'invalid url: ' + url
    
    if site.endswith('.com.cn'):
        site = site[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', site)
    if not domain:
        domain = site
    assert domain, 'unsupported url: ' + url
    
    k = r1(r'([^.]+)', domain)
    downloads = {
        '56': w56,
        'acfun': acfun,
        'bilibili': bilibili,
        'cntv': cntv,
        'dailymotion': dailymotion,
        'google': googleplus,
        'iask': sina,
        'ifeng': ifeng,
        'iqiyi': iqiyi,
        'kankanews': bilibili,
        'ku6': ku6,
        'pptv': pptv,
        'sina': sina,
        'sohu': sohu,
        'tudou': tudou,
        'vimeo': vimeo,
        'yinyuetai': yinyuetai,
        'youku': youku,
        'youtube': youtube,
        #TODO
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

def main():
    script_main('you-get', any_download, any_download_playlist)
