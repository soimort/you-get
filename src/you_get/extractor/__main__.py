#!/usr/bin/env python
__all__ = ['main', 'any_download', 'any_download_playlist']

from ..extractor import *
from ..common import *

def url_to_module(url):
    video_host = r1(r'http://([^/]+)/', url)
    video_url = r1(r'http://[^/]+(.*)', url)
    assert video_host and video_url, 'invalid url: ' + url
    
    if video_host.endswith('.com.cn'):
        video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domain, 'unsupported url: ' + url
    
    k = r1(r'([^.]+)', domain)
    downloads = {
        '163': netease,
        '56': w56,
        '5sing': fivesing,
        'acfun': acfun,
        'baidu': baidu,
        'bilibili': bilibili,
        'blip': blip,
        'cntv': cntv,
        'coursera': coursera,
        'dailymotion': dailymotion,
        'douban': douban,
        'ehow': ehow,
        'facebook': facebook,
        'freesound': freesound,
        'google': google,
        'iask': sina,
        'ifeng': ifeng,
        'in': alive,
        'instagram': instagram,
        'iqiyi': iqiyi,
        'joy': joy,
        'jpopsuki': jpopsuki,
        'kankanews': bilibili,
        'ku6': ku6,
        'letv': letv,
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
        'ted': ted,
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
        'khanacademy': khan,
        #TODO
    }
    if k in downloads:
        return downloads[k]
    else:
        import http.client
        conn = http.client.HTTPConnection(video_host)
        conn.request("HEAD", video_url)
        res = conn.getresponse()
        location = res.getheader('location')
        if location is None:
            raise NotImplementedError(url)
        else:
            return url_to_module(location), location

def any_download(url, output_dir = '.', merge = True, info_only = False):
    try:
        m, url = url_to_module(url)
    except:
        m = url_to_module(url)
    m.download(url, output_dir = output_dir, merge = merge, info_only = info_only)

def any_download_playlist(url, output_dir = '.', merge = True, info_only = False):
    try:
        m, url = url_to_module(url)
    except:
        m = url_to_module(url)
    m.download_playlist(url, output_dir = output_dir, merge = merge, info_only = info_only)

def main():
    script_main('you-get', any_download, any_download_playlist)

if __name__ == "__main__":
    main()
