#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['baidu_download']

from ..common import *
from .. import common

from urllib import parse

def baidu_get_song_data(sid):
    data = json.loads(get_html('http://music.baidu.com/data/music/fmlink?songIds=%s' % sid, faker = True))['data']

    if data['xcode'] != '':
    # inside china mainland
        return data['songList'][0]
    else:
    # outside china mainland
        html = get_html("http://music.baidu.com/song/%s" % sid)

        # baidu pan link
        sourceLink = r1(r'"link-src-info"><a href="([^"]+)"', html)
        if sourceLink != None:
            sourceLink = sourceLink.replace('&amp;', '&')
        sourceHtml = get_html(sourceLink) if sourceLink != None else None

        songLink =  r1(r'\\"dlink\\":\\"([^"]*)\\"', sourceHtml).replace('\\\\/', '/') if sourceHtml != None else r1(r'download_url="([^"]+)"', html)
        songName = parse.unquote(r1(r'songname=([^&]+)&', html))
        artistName = parse.unquote(r1(r'songartistname=([^&]+)&', html))
        albumName = parse.unquote(r1(r'songartistname=([^&]+)&', html))
        lrcLink = r1(r'data-lyricdata=\'{ "href":"([^"]+)"', html)

        return json.loads(json.dumps({'songLink'   : songLink,
                                      'songName'   : songName,
                                      'artistName' : artistName,
                                      'albumName'  : albumName,
                                      'lrcLink'    : lrcLink}, ensure_ascii=False))

def baidu_get_song_url(data):
    return data['songLink']

def baidu_get_song_artist(data):
    return data['artistName']

def baidu_get_song_album(data):
    return data['albumName']

def baidu_get_song_title(data):
    return data['songName']

def baidu_get_song_lyric(data):
    lrc = data['lrcLink']
    return None if lrc is '' else "http://music.baidu.com%s" % lrc

def baidu_download_song(sid, output_dir = '.', merge = True, info_only = False):
    data = baidu_get_song_data(sid)
    url = baidu_get_song_url(data)
    title = baidu_get_song_title(data)
    artist = baidu_get_song_artist(data)
    album = baidu_get_song_album(data)
    lrc = baidu_get_song_lyric(data)

    assert url
    file_name = "%s - %s - %s" % (title, album, artist)

    type, ext, size = url_info(url, faker = True)
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], file_name, ext, size, output_dir, merge = merge, faker = True)

    if lrc:
        type, ext, size = url_info(lrc, faker = True)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([lrc], file_name, ext, size, output_dir, faker = True)

def baidu_download_album(aid, output_dir = '.', merge = True, info_only = False):
    html = get_html('http://music.baidu.com/album/%s' % aid, faker = True)
    album_name = r1(r'<h2 class="album-name">(.+?)<\/h2>', html)
    artist = r1(r'<span class="author_list" title="(.+?)">', html)
    output_dir = '%s/%s - %s' % (output_dir, artist, album_name)
    ids = json.loads(r1(r'<span class="album-add" data-adddata=\'(.+?)\'>', html).replace('&quot', '').replace(';', '"'))['ids']
    track_nr = 1
    for id in ids:
        song_data = baidu_get_song_data(id)
        song_url = baidu_get_song_url(song_data)
        song_title = baidu_get_song_title(song_data)
        song_lrc = baidu_get_song_lyric(song_data)
        file_name = '%02d.%s' % (track_nr, song_title)

        type, ext, size = url_info(song_url, faker = True)
        print_info(site_info, song_title, type, size)
        if not info_only:
            download_urls([song_url], file_name, ext, size, output_dir, merge = merge, faker = True)

        if song_lrc:
            type, ext, size = url_info(song_lrc, faker = True)
            print_info(site_info, song_title, type, size)
            if not info_only:
                download_urls([song_lrc], file_name, ext, size, output_dir, faker = True)

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
