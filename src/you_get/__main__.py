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
        '163': netease,
        '56': w56,
        'acfun': acfun,
        'baidu': baidu,
        'bilibili': bilibili,
        'blip': blip,
        'cntv': cntv,
        'coursera': coursera,
        'dailymotion': dailymotion,
        'douban': douban,
        'facebook': facebook,
        'freesound': freesound,
        'google': google,
        'iask': sina,
        'ifeng': ifeng,
        'in': alive,
        'instagram': instagram,
        'iqiyi': iqiyi,
        'joy': joy,
        'kankanews': bilibili,
        'ku6': ku6,
        'miomio': miomio,
        'mixcloud': mixcloud,
        'nicovideo': nicovideo,
        'pptv': pptv,
        'qq': qq,
        'sina': sina,
        'smgbb': bilibili,
        'sohu': sohu,
        'songtaste':songtaste,
        'soundcloud': soundcloud,
        'tudou': tudou,
        'tumblr': tumblr,
        'vid48': vid48,
        'vimeo': vimeo,
        'vine': vine,
        'xiami': xiami,
        'yinyuetai': yinyuetai,
        'youku': youku,
        'youtu': youtube,
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

if __name__ == "__main__":
    main()
