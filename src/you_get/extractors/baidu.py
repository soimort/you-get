#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['baidu_download']

from ..common import *
from .embed import *
from .universal import *

def baidu_get_song_data(sid):
    data = json.loads(get_html('http://music.baidu.com/data/music/fmlink?songIds=%s' % sid, faker = True))['data']

    if data['xcode'] != '':
        # inside china mainland
        return data['songList'][0]
    else:
        # outside china mainland
        return None

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

def baidu_download_song(sid, output_dir='.', merge=True, info_only=False):
    data = baidu_get_song_data(sid)
    if data is not None:
        url = baidu_get_song_url(data)
        title = baidu_get_song_title(data)
        artist = baidu_get_song_artist(data)
        album = baidu_get_song_album(data)
        lrc = baidu_get_song_lyric(data)
        file_name = "%s - %s - %s" % (title, album, artist)
    else:
        html = get_html("http://music.baidu.com/song/%s" % sid)
        url = r1(r'data_url="([^"]+)"', html)
        title = r1(r'data_name="([^"]+)"', html)
        file_name = title

    type, ext, size = url_info(url, faker=True)
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], file_name, ext, size, output_dir, merge=merge, faker=True)

    try:
        type, ext, size = url_info(lrc, faker=True)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([lrc], file_name, ext, size, output_dir, faker=True)
    except:
        pass

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

def baidu_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False, **kwargs):
    if re.match(r'http://imgsrc.baidu.com', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only)
        return

    elif re.match(r'http://pan.baidu.com', url):
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

    elif re.match('http://tieba.baidu.com/', url):
        try:
            # embedded videos
            embed_download(url, output_dir, merge=merge, info_only=info_only)
        except:
            # images
            html = get_html(url)
            title = r1(r'title:"([^"]+)"', html)

            items = re.findall(r'//imgsrc.baidu.com/forum/w[^"]+/([^/"]+)', html)
            urls = ['http://imgsrc.baidu.com/forum/pic/item/' + i
                    for i in set(items)]

            # handle albums
            kw = r1(r'kw=([^&]+)', html) or r1(r"kw:'([^']+)'", html)
            tid = r1(r'tid=(\d+)', html) or r1(r"tid:'([^']+)'", html)
            album_url = 'http://tieba.baidu.com/photo/g/bw/picture/list?kw=%s&tid=%s' % (kw, tid)
            album_info = json.loads(get_content(album_url))
            for i in album_info['data']['pic_list']:
                urls.append('http://imgsrc.baidu.com/forum/pic/item/' + i['pic_id'] + '.jpg')

            ext = 'jpg'
            size = float('Inf')
            print_info(site_info, title, ext, size)

            if not info_only:
                download_urls(urls, title, ext, size,
                              output_dir=output_dir, merge=False)

site_info = "Baidu.com"
download = baidu_download
download_playlist = playlist_not_supported("baidu")
