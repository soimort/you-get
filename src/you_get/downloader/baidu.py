#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['baidu_download']

from ..common import *
from .. import common

from urllib import parse

def baidu_get_song_html(sid):
    return get_html('http://music.baidu.com/song/%s/download?__o=%%2Fsong%%2F%s' % (sid, sid), faker = True)

def baidu_get_song_url(html):
    return r1(r'downlink="/data/music/file\?link=(.+?)"', html)

def baidu_get_song_artist(html):
    return r1(r'singer_name:"(.+?)"', html)

def baidu_get_song_album(html):
    return r1(r'ablum_name:"(.+?)"', html)

def baidu_get_song_title(html):
    return r1(r'song_title:"(.+?)"', html)

def baidu_download_lyric(sid, file_name, output_dir):
    if common.dry_run:
        return

    html = get_html('http://music.baidu.com/song/' + sid)
    href = r1(r'<a class="down-lrc-btn" data-lyricdata=\'{ "href":"(.+?)" }\' href="#">', html)
    if href:
        lrc = get_html('http://music.baidu.com' + href)
        if len(lrc) > 0:
            with open(output_dir + "/" + file_name.replace('/', '-') + '.lrc', 'w') as x:
                x.write(lrc)

def baidu_download_song(sid, output_dir = '.', merge = True, info_only = False):
    html = baidu_get_song_html(sid)
    url = baidu_get_song_url(html)
    title = baidu_get_song_title(html)
    artist = baidu_get_song_artist(html)
    album = baidu_get_song_album(html)
    type, ext, size = url_info(url, faker = True)
    print_info(site_info, title, type, size)
    if not info_only:
        file_name = "%s - %s - %s" % (title, album, artist)
        download_urls([url], file_name, ext, size, output_dir, merge = merge, faker = True)
        baidu_download_lyric(sid, file_name, output_dir)

def baidu_download_album(aid, output_dir = '.', merge = True, info_only = False):
    html = get_html('http://music.baidu.com/album/%s' % aid, faker = True)
    album_name = r1(r'<h2 class="album-name">(.+?)<\/h2>', html)
    artist = r1(r'<span class="author_list" title="(.+?)">', html)
    output_dir = '%s/%s - %s' % (output_dir, artist, album_name)
    ids = json.loads(r1(r'<span class="album-add" data-adddata=\'(.+?)\'>', html).replace('&quot', '').replace(';', '"'))['ids']
    track_nr = 1
    for id in ids:
        song_html = baidu_get_song_html(id)
        song_url = baidu_get_song_url(song_html)
        song_title = baidu_get_song_title(song_html)
        file_name = '%02d.%s' % (track_nr, song_title)
        type, ext, size = url_info(song_url, faker = True)
        print_info(site_info, song_title, type, size)
        if not info_only:
            download_urls([song_url], file_name, ext, size, output_dir, merge = merge, faker = True)
            baidu_download_lyric(id, file_name, output_dir)
        track_nr += 1

def baidu_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False):
    if re.match(r'http://pan.baidu.com', url):
        html = get_html(url)
        
        title = r1(r'server_filename="([^"]+)"', html)
        if len(title.split('.')) > 1:
            title = ".".join(title.split('.')[:-1])
        
        real_url = r1(r'\\"dlink\\":\\"([^"]*)\\"', html).replace('\\\\/', '/')
        type, ext, size = url_info(real_url, faker = True)
        
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([real_url], title, ext, size, output_dir, merge = merge)
    
    elif re.match(r'http://music.baidu.com/album/\d+', url):
        id = r1(r'http://music.baidu.com/album/(\d+)', url)
        baidu_download_album(id, output_dir, merge, info_only)

    elif re.match('http://music.baidu.com/song/\d+', url):
        id = r1(r'http://music.baidu.com/song/(\d+)', url)
        baidu_download_song(id, output_dir, merge, info_only)

site_info = "Baidu.com"
download = baidu_download
download_playlist = playlist_not_supported("baidu")
