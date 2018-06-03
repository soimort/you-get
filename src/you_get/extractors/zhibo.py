#!/usr/bin/env python

__all__ = ['zhibo_download']

from ..common import *

def zhibo_vedio_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    # http://video.zhibo.tv/video/details/d103057f-663e-11e8-9d83-525400ccac43.html

    html = get_html(url)
    title = r1(r'<title>([\s\S]*)</title>', html)
    total_size = 0
    part_urls= []

    video_html = r1(r'<script type="text/javascript">([\s\S]*)</script></head>', html)

    # video_guessulike = r1(r"window.xgData =([s\S'\s\.]*)\'\;[\s\S]*window.vouchData", video_html) 
    video_url = r1(r"window.vurl = \'([s\S'\s\.]*)\'\;[\s\S]*window.imgurl", video_html)
    part_urls.append(video_url)
    ext = video_url.split('.')[-1]

    print_info(site_info, title, ext, total_size)
    if not info_only:
        download_urls(part_urls, title, ext, total_size, output_dir=output_dir, merge=merge)


def zhibo_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if 'video.zhibo.tv' in url:
        zhibo_vedio_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    # if 'v.zhibo.tv' in url:
    # http://v.zhibo.tv/31609372
    html = get_html(url)
    title = r1(r'<title>([\s\S]*)</title>', html)
    is_live = r1(r"window.videoIsLive=\'([s\S'\s\.]*)\'\;[\s\S]*window.resDomain", html)
    if is_live is not "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % is_live)

    ourStreamName = r1(r"window.ourStreamName=\'([s\S'\s\.]*)\'\;[\s\S]*window.rtmpDefaultSource", html)
    rtmpPollUrl = r1(r"window.rtmpPollUrl=\'([s\S'\s\.]*)\'\;[\s\S]*window.hlsDefaultSource", html)

    #real_url = 'rtmp://220.194.213.56/live.zhibo.tv/8live/' + ourStreamName
    real_url = rtmpPollUrl + ourStreamName

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', params={}, output_dir=output_dir, merge=merge)

site_info = "zhibo.tv"
download = zhibo_download
download_playlist = playlist_not_supported('zhibo')
