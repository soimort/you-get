# -*- coding: utf-8 -*-

__all__ = ['dongting_download']

from ..common import *

_unit_prefixes = 'bkmg'

def parse_size(size):
    m = re.match(r'([\d.]+)(.(?:i?B)?)', size, re.I)
    if m:
        return int(float(m.group(1)) * 1024 **
                   _unit_prefixes.index(m.group(2).lower()))
    else:
        return 0

def dongting_download_lyric(lrc_url, file_name, output_dir):
    j = get_html(lrc_url)
    info = json.loads(j)
    lrc = j['data']['lrc']
    filename = get_filename(file_name)
    with open(output_dir + "/" + filename + '.lrc', 'w', encoding='utf-8') as x:
        x.write(lrc)

def dongting_download_song(sid, output_dir = '.', merge = True, info_only = False):
    j = get_html('http://ting.hotchanson.com/detail.do?neid=%s&size=0' % sid)
    info = json.loads(j)

    song_title = info['data']['songName']
    album_name = info['data']['albumName']
    artist = info['data']['singerName']
    ext = 'mp3'
    size = parse_size(info['data']['itemList'][-1]['size'])
    url = info['data']['itemList'][-1]['downUrl']

    print_info(site_info, song_title, ext, size)
    if not info_only:
        file_name = "%s - %s - %s" % (song_title, album_name, artist)
        download_urls([url], file_name, ext, size, output_dir, merge = merge)
        lrc_url = ('http://lp.music.ttpod.com/lrc/down?'
                   'lrcid=&artist=%s&title=%s') % (
                       parse.quote(artist), parse.quote(song_title))
        try:
            dongting_download_lyric(lrc_url, file_name, output_dir)
        except:
            pass

def dongting_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False, **kwargs):
    if re.match('http://www.dongting.com/\?song_id=\d+', url):
        id = r1(r'http://www.dongting.com/\?song_id=(\d+)', url)
        dongting_download_song(id, output_dir, merge, info_only)

site_info = "Dongting.com"
download = dongting_download
download_playlist = playlist_not_supported("dongting")
