#!/usr/bin/env python


__all__ = ['netease_download']

from ..common import *
from ..common import print_more_compatible as print
from ..util import fs,pyaes
from json import loads
import hashlib
import base64
import os
import binascii
try:
    from Crypto.Cipher import AES
except:
    print("No Crypto Modulu")
import requests

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
        #print(j)
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
        j = loads(get_content("http://music.163.com/api/playlist/detail?id=%s&csrf_token=" % rid, headers={"Referer": "http://music.163.com/"}))

        new_dir = output_dir + '/' + fs.legitimize(j['result']['name'])
        if not info_only:
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            cover_url = j['result']['coverImgUrl']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)
        
        prefix_width = len(str(len(j['result']['tracks'])))
        for n, i in enumerate(j['result']['tracks']):
            playlist_prefix = '%%.%dd_' % prefix_width % n
            netease_song_download(i, output_dir=new_dir, info_only=info_only, playlist_prefix=playlist_prefix)
            try: # download lyrics
                assert kwargs['caption']
                l = loads(get_content("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % i['id'], headers={"Referer": "http://music.163.com/"}))
                netease_lyric_download(i, l["lrc"]["lyric"], output_dir=new_dir, info_only=info_only, playlist_prefix=playlist_prefix)
            except: pass

    elif "song" in url:
        song = get_song_by_id(rid)
        netease_song_download(song, output_dir=output_dir, info_only=info_only)
        try: # download lyrics
            assert kwargs['caption']
            netease_lyric_download(song, song["lrc"]["lyric"], output_dir=output_dir, info_only=info_only)
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

    title = song['detail']['name']+'-'+song['detail']['ar'][0]['name']
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
    title = song['detail']['name']+'-'+song['detail']['ar'][0]['name']
    url_best = song["src"]['url']
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

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    aes = pyaes.AESModeOfOperationCBC(secKey.encode(), b'0102030405060708')
    ciphertext = aes.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int( binascii.hexlify(text.encode()), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def get_song_by_id(id):
    song_detail_text = '{"id":"%s","c":"[{\\"id\\":\\"%s\\"}]","csrf_token":""}'%(id,id)
    ## modulus，nonce and pubKey get from https://s3.music.126.net/web/s/core.js?5539de95b51f251999079b35d1260395
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    secKey = "TF8V0U3Juw8M9A1g"

    song_src    = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    song_detail = 'https://music.163.com/weapi/v3/song/detail?csrf_token='
    song_lyric = 'https://music.163.com/weapi/song/lyric?csrf_token='

    detail_encText = aesEncrypt(aesEncrypt(song_detail_text, nonce).decode(), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    ## post data
    data = {
        'params': detail_encText,
        'encSecKey': encSecKey
    }
    ## headers for cheating webserver
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    ## get detail of song
    # res_detail = post_content(song_detail,post_data=data,headers=headers,decoded=False)
    res_detail = post_content(song_detail,post_data = data,headers =headers)
    detail = loads(res_detail)['songs'][0]
    br = 320000
    if('h' in detail.keys() and detail['h']!=None):
        print("h")
        br = detail['h']['br']
    elif('m' in detail.keys() and detail['m']!=None):
        br = detail['m']['br']
    elif('l' in detail.keys() and detail['l']!=None):
        br = detail['l']['br']

    song_text = '{"ids":"[%s]","br":%d,"csrf_token":""}'%(id,br)

    #compute song encText 
    song_encText = aesEncrypt(aesEncrypt(song_text, nonce).decode(), secKey)
    data['params'] = song_encText

    # get download url of song
    res_song = post_content(song_src,post_data=data,headers = headers)
    song = loads(res_song)
    ## get lyriic
    lyric_text = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}'%(id)
    lyric_encText = aesEncrypt(aesEncrypt(lyric_text, nonce).decode(), secKey)
    data['params'] = lyric_encText
    res_lyric = post_content(song_lyric,post_data=data,headers=headers)
    lyric = loads(res_lyric)

    # return song info
    song_info = {}
    song_info["src"] = song['data'][0]
    song_info["detail"] = detail
    song_info['lrc'] = lyric['lrc']
    return song_info

site_info = "163.com"
download = netease_download
download_playlist = playlist_not_supported('netease')
