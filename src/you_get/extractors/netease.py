#!/usr/bin/env python


__all__ = ['netease_download']

from ..common import *
from ..common import print_more_compatible as print
from ..util import fs
from json import loads
import hashlib
import base64
import os
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB

def netease_hymn():
    return """
    player's Game Over,
    u can abandon.
    u get pissed,
    get pissed,
    Hallelujah my King!
    errr oh! fuck ohhh!!!!
    """

def netease_cloud_music_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    rid = match1(url, r'\Wid=(.*)')
    if rid is None:
        rid = match1(url, r'/(\d+)/?')
    if "album" in url:
        j = loads(get_content("http://music.163.com/api/album/%s?id=%s&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))

        artist_name = j['album']['artists'][0]['name']
        album_name = j['album']['name'].strip()
        new_dir = output_dir + '/' + fs.legitimize("%s - %s" % (artist_name, album_name))
        if not info_only:
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            cover_url = j['album']['picUrl']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)

        for i in j['album']['songs']:
            netease_song_download(i, output_dir=new_dir, info_only=info_only)
            try: # download lyrics
                assert kwargs['caption']
                l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % i['id'], headers={"Referer": "http://music.163.com/"}))
                netease_lyric_download(i, l["lrc"]["lyric"], output_dir=new_dir, info_only=info_only)
            except: pass

    elif "playlist" in url:
        j = loads(get_content("https://api.imjad.cn/cloudmusic/?type=playlist&id=%s" % rid, headers={"Referer": "http://music.163.com/"}))
        new_dir = output_dir + '/' + fs.legitimize(j['playlist']['name'])
        if not info_only:
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            cover_url = j['playlist']['coverImgUrl']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)
        
        prefix_width = len(str(len(j['playlist']['tracks'])))
        for n, i in enumerate(j['playlist']['tracks']):
            playlist_prefix = '%%.%dd_' % prefix_width % n
            this_song_api_result = loads(get_content("http://music.163.com/api/song/detail/?id=%s&ids=[%s]&csrf_token=" % (i['id'], i['id']), headers={"Referer": "http://music.163.com/"}))
            netease_song_download(this_song_api_result['songs'][0], output_dir=new_dir, info_only=info_only, playlist_prefix=playlist_prefix)
            try: # download lyrics
                assert kwargs['caption']
                l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % i['id'], headers={"Referer": "http://music.163.com/"}))
                netease_lyric_download(this_song_api_result['songs'][0], l["lrc"]["lyric"], output_dir=new_dir, info_only=info_only, playlist_prefix=playlist_prefix)
            except: pass

    elif "song" in url:
        j = loads(get_content("http://music.163.com/api/song/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        netease_song_download(j["songs"][0], output_dir=output_dir, info_only=info_only)
        try: # download lyrics
            assert kwargs['caption']
            l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % rid, headers={"Referer": "http://music.163.com/"}))
            netease_lyric_download(j["songs"][0], l["lrc"]["lyric"], output_dir=output_dir, info_only=info_only)
        except: pass

    elif "program" in url:
        j = loads(get_content("http://music.163.com/api/dj/program/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        netease_song_download(j["program"]["mainSong"], output_dir=output_dir, info_only=info_only)

    elif "radio" in url:
        j = loads(get_content("http://music.163.com/api/dj/program/byradio/?radioId=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        for i in j['programs']:
            netease_song_download(i["mainSong"],output_dir=output_dir, info_only=info_only)

    elif "mv" in url:
        j = loads(get_content("http://music.163.com/api/mv/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid), headers={"Referer": "http://music.163.com/"}))
        netease_video_download(j['data'], output_dir=output_dir, info_only=info_only)

def netease_lyric_download(song, lyric, output_dir='.', info_only=False, playlist_prefix=""):
    if info_only: return

    title = "%s%s. %s" % (playlist_prefix, song['position'], song['name'])
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

def netease_song_download(song, output_dir='.', info_only=False, playlist_prefix=""):
    print(song)
    title = "%s%s. %s" % (playlist_prefix, song['position'], song['name'])
    url_best = "http://music.163.com/song/media/outer/url?id=" + \
        str(song['id']) + ".mp3"
    '''
    songNet = 'p' + song['mp3Url'].split('/')[2][1:]

    if 'hMusic' in song and song['hMusic'] != None:
        url_best = make_url(songNet, song['hMusic']['dfsId'])
    elif 'mp3Url' in song:
        url_best = song['mp3Url']
    elif 'bMusic' in song:
        url_best = make_url(songNet, song['bMusic']['dfsId'])
    '''
    netease_download_common(title, url_best,
                            output_dir=output_dir, info_only=info_only)
    '''
    Here is my changes
    '''
    api_result = requests.get('https://api.imjad.cn/cloudmusic/?type=detail&id='+str(song['id']))
    song_info = json.loads(api_result.text)['songs'][0]
    songtype, ext, size = url_info(url_best, faker=True)
    xiaokang00010_changed_ext = ext
    if xiaokang00010_changed_ext == None:
        xiaokang00010_changed_ext = 'None'
    # build song infomations
    artists = ''
    # al.picUrl
    song_cover = requests.get(song_info['al']['picUrl'])
    # build artists
    for i in song_info['ar']:
        artists = artists + i['name'] + '/'
    print(output_dir + '/' + get_output_filename(url_best, tr(get_filename(title)), ext, output_dir, True))
    songFile = ID3( output_dir + '/' + get_output_filename(url_best, tr(get_filename(title)), ext, output_dir, True) )
    songFile['TIT2'] = TIT2(  # 插入歌名
        encoding=3,
        text=song_info['name']
    )
    songFile['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
        encoding=3,
        text=artists[0:-1]
    )
    songFile['TALB'] = TALB(  # 插入专辑名
        encoding=3,
        text=song_info['al']['name']
    )
    songFile['APIC'] = APIC(  # 插入封面
        encoding=3,
        mime='image/jpeg',
        type=3,
        desc=u'Cover',
        data=song_cover.content
    )
    songFile.save()
    #print('Netease Music Downloader (Xiaokang00010 Edited)\n--- Thanks for using! ---\nAuto import music infomation success.')

def netease_download_common(title, url_best, output_dir, info_only):
    songtype, ext, size = url_info(url_best, faker=True)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url_best], title, ext, size, output_dir, faker=True)


def netease_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if "163.fm" in url:
        url = get_location(url)
    if "music.163.com" in url:
        netease_cloud_music_download(url, output_dir, merge, info_only, **kwargs)
    else:
        html = get_decoded_html(url)

        title = r1('movieDescription=\'([^\']+)\'', html) or r1('<title>(.+)</title>', html)

        if title[0] == ' ':
            title = title[1:]

        src = r1(r'<source src="([^"]+)"', html) or r1(r'<source type="[^"]+" src="([^"]+)"', html)

        if src:
            url = src
            _, ext, size = url_info(src)
            #sd_url = r1(r'(.+)-mobile.mp4', src) + ".flv"
            #hd_url = re.sub('/SD/', '/HD/', sd_url)

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


def make_url(songNet, dfsId):
    encId = encrypted_id(dfsId)
    mp3_url = "http://%s/%s/%s.mp3" % (songNet, encId, dfsId)
    return mp3_url


site_info = "163.com"
download = netease_download
download_playlist = playlist_not_supported('netease')
