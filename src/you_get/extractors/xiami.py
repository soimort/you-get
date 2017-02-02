#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['xiami_download']

from ..common import *

from xml.dom.minidom import parseString
from urllib import parse

def location_dec(str):
    head = int(str[0])
    str = str[1:]
    rows = head
    cols = int(len(str)/rows) + 1

    out = ""
    full_row = len(str) % head
    for c in range(cols):
        for r in range(rows):
            if c == (cols - 1) and r >= full_row:
                continue
            if r < full_row:
                char = str[r*cols+c]
            else:
                char = str[cols*full_row+(r-full_row)*(cols-1)+c]
            out += char
    return parse.unquote(out).replace("^", "0")

def xiami_download_lyric(lrc_url, file_name, output_dir):
    lrc = get_html(lrc_url, faker = True)
    filename = get_filename(file_name)
    if len(lrc) > 0:
        with open(output_dir + "/" + filename + '.lrc', 'w', encoding='utf-8') as x:
            x.write(lrc)

def xiami_download_pic(pic_url, file_name, output_dir):
    pic_url = pic_url.replace('_1', '')
    pos = pic_url.rfind('.')
    ext = pic_url[pos:]
    pic = get_response(pic_url, faker = True).data
    if len(pic) > 0:
        with open(output_dir + "/" + file_name.replace('/', '-') + ext, 'wb') as x:
            x.write(pic)

def xiami_download_song(sid, output_dir = '.', merge = True, info_only = False):
    xml = get_html('http://www.xiami.com/song/playlist/id/%s/object_name/default/object_id/0' % sid, faker = True)
    doc = parseString(xml)
    i = doc.getElementsByTagName("track")[0]
    artist = i.getElementsByTagName("artist")[0].firstChild.nodeValue
    album_name = i.getElementsByTagName("album_name")[0].firstChild.nodeValue
    song_title = i.getElementsByTagName("title")[0].firstChild.nodeValue
    url = location_dec(i.getElementsByTagName("location")[0].firstChild.nodeValue)
    try:
        lrc_url = i.getElementsByTagName("lyric")[0].firstChild.nodeValue
    except:
        pass
    type, ext, size = url_info(url, faker = True)
    if not ext:
        ext = 'mp3'

    print_info(site_info, song_title, ext, size)
    if not info_only:
        file_name = "%s - %s - %s" % (song_title, artist, album_name)
        download_urls([url], file_name, ext, size, output_dir, merge = merge, faker = True)
        try:
            xiami_download_lyric(lrc_url, file_name, output_dir)
        except:
            pass

def xiami_download_showcollect(cid, output_dir = '.', merge = True, info_only = False):
    html = get_html('http://www.xiami.com/song/showcollect/id/' + cid, faker = True)
    collect_name = r1(r'<title>(.*)</title>', html)

    xml = get_html('http://www.xiami.com/song/playlist/id/%s/type/3' % cid, faker = True)
    doc = parseString(xml)
    output_dir =  output_dir + "/" + "[" + collect_name + "]"
    tracks = doc.getElementsByTagName("track")
    track_nr = 1
    for i in tracks:
        artist=album_name=song_title=url=""
        try:
            song_id = i.getElementsByTagName("song_id")[0].firstChild.nodeValue
            artist = i.getElementsByTagName("artist")[0].firstChild.nodeValue
            album_name = i.getElementsByTagName("album_name")[0].firstChild.nodeValue
            song_title = i.getElementsByTagName("title")[0].firstChild.nodeValue
            url = location_dec(i.getElementsByTagName("location")[0].firstChild.nodeValue)
        except:
            log.e("Song %s failed. [Info Missing] artist:%s, album:%s, title:%s, url:%s" % (song_id, artist, album_name, song_title, url))
            continue
        try:
            lrc_url = i.getElementsByTagName("lyric")[0].firstChild.nodeValue
        except:
            pass
        type, ext, size = url_info(url, faker = True)
        if not ext:
            ext = 'mp3'

        print_info(site_info, song_title, type, size)
        if not info_only:
            file_name = "%02d.%s - %s - %s" % (track_nr, song_title, artist, album_name)
            download_urls([url], file_name, ext, size, output_dir, merge = merge, faker = True)
            try:
                xiami_download_lyric(lrc_url, file_name, output_dir)
            except:
                pass

        track_nr += 1

def xiami_download_album(aid, output_dir = '.', merge = True, info_only = False):
    xml = get_html('http://www.xiami.com/song/playlist/id/%s/type/1' % aid, faker = True)
    album_name = r1(r'<album_name><!\[CDATA\[(.*)\]\]>', xml)
    artist = r1(r'<artist><!\[CDATA\[(.*)\]\]>', xml)
    doc = parseString(xml)
    output_dir = output_dir + "/%s - %s" % (artist, album_name)
    tracks = doc.getElementsByTagName("track")
    track_nr = 1
    pic_exist = False
    for i in tracks:
        song_title = i.getElementsByTagName("title")[0].firstChild.nodeValue
        url = location_dec(i.getElementsByTagName("location")[0].firstChild.nodeValue)
        try:
            lrc_url = i.getElementsByTagName("lyric")[0].firstChild.nodeValue
        except:
            pass
        if not pic_exist:
            pic_url = i.getElementsByTagName("pic")[0].firstChild.nodeValue
        type, ext, size = url_info(url, faker = True)
        if not ext:
            ext = 'mp3'

        print_info(site_info, song_title, type, size)
        if not info_only:
            file_name = "%02d.%s" % (track_nr, song_title)
            download_urls([url], file_name, ext, size, output_dir, merge = merge, faker = True)
            try:
                xiami_download_lyric(lrc_url, file_name, output_dir)
            except:
                pass
            if not pic_exist:
                xiami_download_pic(pic_url, 'cover', output_dir)
                pic_exist = True

        track_nr += 1

def xiami_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False, **kwargs):
    if re.match(r'http://www.xiami.com/album/\d+', url):
        id = r1(r'http://www.xiami.com/album/(\d+)', url)
        xiami_download_album(id, output_dir, merge, info_only)

    if re.match(r'http://www.xiami.com/collect/\d+', url):
        id = r1(r'http://www.xiami.com/collect/(\d+)', url)
        xiami_download_showcollect(id, output_dir, merge, info_only)

    if re.match('http://www.xiami.com/song/\d+', url):
        html = get_html(url, faker=True)
        id = r1(r'rel="canonical" href="http://www.xiami.com/song/([^"]+)"', html)
        xiami_download_song(id, output_dir, merge, info_only)

    if re.match('http://www.xiami.com/song/detail/id/\d+', url):
        id = r1(r'http://www.xiami.com/song/detail/id/(\d+)', url)
        xiami_download_song(id, output_dir, merge, info_only)

site_info = "Xiami.com"
download = xiami_download
download_playlist = playlist_not_supported("xiami")
