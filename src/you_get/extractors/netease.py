#!/usr/bin/env python


__all__ = ['netease_download']

from ..common import *
from json import loads
import hashlib
import base64
import os

def netease_hymn():
    return """
    player's Game Over,
    u can abandon.
    u get pissed,
    get pissed,
    Hallelujah my King!
    errr oh! fuck ohhh!!!!
    """

def netease_cloud_music_download(url, output_dir='.', merge=True, info_only=False):
    rid = match1(url, r'id=(.*)')
    if rid is None:
        rid = match1(url, r'/(\d+)/?$')
    if "album" in url:
        j = loads(get_content("http://music.163.com/api/album/%s?id=%s&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))

        artist_name = j['album']['artists'][0]['name']
        album_name = j['album']['name']
        new_dir = output_dir + '/' + "%s - %s" % (artist_name, album_name)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        if not info_only:
            cover_url = j['album']['picUrl']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)

        for i in j['album']['songs']:
            netease_song_download(i, output_dir=new_dir, info_only=info_only)
            try: # download lyrics
                l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % i['id'], headers={"Referer": "http://music.163.com/"}))
                netease_lyric_download(i, l["lrc"]["lyric"], output_dir=new_dir, info_only=info_only)
            except: pass

    elif "playlist" in url:
        j = loads(get_content("http://music.163.com/api/playlist/detail?id=%s&csrf_token=" % rid, headers={"Referer": "http://music.163.com/"}))

        new_dir = output_dir + '/' + j['result']['name']
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        if not info_only:
            cover_url = j['result']['coverImgUrl']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)

        for i in j['result']['tracks']:
            netease_song_download(i, output_dir=new_dir, info_only=info_only)
            try: # download lyrics
                l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % i['id'], headers={"Referer": "http://music.163.com/"}))
                netease_lyric_download(i, l["lrc"]["lyric"], output_dir=new_dir, info_only=info_only)
            except: pass

    elif "song" in url:
        j = loads(get_content("http://music.163.com/api/song/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        netease_song_download(j["songs"][0], output_dir=output_dir, info_only=info_only)
        try: # download lyrics
            l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % rid, headers={"Referer": "http://music.163.com/"}))
            netease_lyric_download(j["songs"][0], l["lrc"]["lyric"], output_dir=output_dir, info_only=info_only)
        except: pass

    elif "mv" in url:
        j = loads(get_content("http://music.163.com/api/mv/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        netease_video_download(j['data'], output_dir=output_dir, info_only=info_only)

def netease_lyric_download(song, lyric, output_dir='.', info_only=False):
    if info_only: return

    title = "%s. %s" % (song['position'], song['name'])
    filename = '%s.lrc' % get_filename(title)
    print('Saving %s ...' % filename, end="", flush=True)
    with open(os.path.join(output_dir, filename),
              'w', encoding='utf-8') as x:
        x.write(lyric)
        print('Done.')

def netease_video_download(vinfo, output_dir='.', info_only=False):
    title = "%s - %s" % (vinfo['name'], vinfo['artistName'])
    url_best = sorted(vinfo["brs"].items(), reverse=True,
                      key=lambda x: int(x[0]))[0][1]
    netease_download_common(title, url_best,
                            output_dir=output_dir, info_only=info_only)

def netease_song_download(song, output_dir='.', info_only=False):
    title = "%s. %s" % (song['position'], song['name'])

    if 'hMusic' in song and song['hMusic'] != None:
        url_best = make_url(song['hMusic']['dfsId'])
    elif 'mp3Url' in song:
        url_best = song['mp3Url']
    elif 'bMusic' in song:
        url_best = make_url(song['bMusic']['dfsId'])

    netease_download_common(title, url_best,
                            output_dir=output_dir, info_only=info_only)

def netease_download_common(title, url_best, output_dir, info_only):
    songtype, ext, size = url_info(url_best)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url_best], title, ext, size, output_dir)


def netease_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if "163.fm" in url:
        url = get_location(url)
    if "music.163.com" in url:
        netease_cloud_music_download(url,output_dir,merge,info_only)
    else:
        html = get_decoded_html(url)

        title = r1('movieDescription=\'([^\']+)\'', html) or r1('<title>(.+)</title>', html)

        if title[0] == ' ':
            title = title[1:]

        src = r1(r'<source src="([^"]+)"', html) or r1(r'<source type="[^"]+" src="([^"]+)"', html)

        if src:
            sd_url = r1(r'(.+)-mobile.mp4', src) + ".flv"
            _, _, sd_size = url_info(sd_url)

            hd_url = re.sub('/SD/', '/HD/', sd_url)
            _, _, hd_size = url_info(hd_url)

            if hd_size > sd_size:
                url, size = hd_url, hd_size
            else:
                url, size = sd_url, sd_size
            ext = 'flv'

        else:
            url = (r1(r'["\'](.+)-list.m3u8["\']', html) or r1(r'["\'](.+).m3u8["\']', html)) + ".mp4"
            _, _, size = url_info(url)
            ext = 'mp4'

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir = output_dir, merge = merge)


def encrypted_id(dfsId):
    x = [ord(i[0]) for i in netease_hymn().split()]
    y = ''.join([chr(i - 61) if i > 96 else chr(i + 32) for i in x])
    byte1 = bytearray(y, encoding='ascii')
    byte2 = bytearray(str(dfsId), encoding='ascii')
    for i in range(len(byte2)):
        byte2[i] ^= byte1[i % len(byte1)]
    m = hashlib.md5()
    m.update(byte2)
    result = base64.b64encode(m.digest()).decode('ascii')
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result


def make_url(dfsId):
    encId = encrypted_id(dfsId)
    mp3_url = "http://m5.music.126.net/%s/%s.mp3" % (encId, dfsId)
    return mp3_url


site_info = "163.com"
download = netease_download
download_playlist = playlist_not_supported('netease')
