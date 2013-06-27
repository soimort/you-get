#!/usr/bin/env python

__all__ = ['youtube_download', 'youtube_download_by_id']

from ..common import *

# YouTube media encoding options, in descending quality order.
# taken from http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs, 3/22/2013.
youtube_codecs = [
    {'itag': 38, 'container': 'MP4', 'video_resolution': '3072p', 'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3.5-5', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
    {'itag': 46, 'container': 'WebM', 'video_resolution': '1080p', 'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
    {'itag': 37, 'container': 'MP4', 'video_resolution': '1080p', 'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3-4.3', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
    {'itag': 102, 'container': '', 'video_resolution': '', 'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '2', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
    {'itag': 45, 'container': 'WebM', 'video_resolution': '720p', 'video_encoding': '', 'video_profile': '', 'video_bitrate': '', 'audio_encoding': '', 'audio_bitrate': ''},
    {'itag': 22, 'container': 'MP4', 'video_resolution': '720p', 'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '2-2.9', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
    {'itag': 84, 'container': 'MP4', 'video_resolution': '720p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '2-2.9', 'audio_encoding': 'AAC', 'audio_bitrate': '152'},
    {'itag': 120, 'container': 'FLV', 'video_resolution': '720p', 'video_encoding': 'AVC', 'video_profile': 'Main@L3.1', 'video_bitrate': '2', 'audio_encoding': 'AAC', 'audio_bitrate': '128'},
    {'itag': 85, 'container': 'MP4', 'video_resolution': '520p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '2-2.9', 'audio_encoding': 'AAC', 'audio_bitrate': '152'},
    {'itag': 44, 'container': 'WebM', 'video_resolution': '480p', 'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '1', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
    {'itag': 35, 'container': 'FLV', 'video_resolution': '480p', 'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.8-1', 'audio_encoding': 'AAC', 'audio_bitrate': '128'},
    {'itag': 101, 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
    {'itag': 100, 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
    {'itag': 43, 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '0.5', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
    {'itag': 34, 'container': 'FLV', 'video_resolution': '360p', 'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '128'},
    {'itag': 82, 'container': 'MP4', 'video_resolution': '360p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
    {'itag': 18, 'container': 'MP4', 'video_resolution': '270p/360p', 'video_encoding': 'H.264', 'video_profile': 'Baseline', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
    {'itag': 6, 'container': 'FLV', 'video_resolution': '270p', 'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.8', 'audio_encoding': 'MP3', 'audio_bitrate': '64'},
    {'itag': 83, 'container': 'MP4', 'video_resolution': '240p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
    {'itag': 13, 'container': '3GP', 'video_resolution': '', 'video_encoding': 'MPEG-4 Visual', 'video_profile': '', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': ''},
    {'itag': 5, 'container': 'FLV', 'video_resolution': '240p', 'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.25', 'audio_encoding': 'MP3', 'audio_bitrate': '64'},
    {'itag': 36, 'container': '3GP', 'video_resolution': '240p', 'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.17', 'audio_encoding': 'AAC', 'audio_bitrate': '38'},
    {'itag': 17, 'container': '3GP', 'video_resolution': '144p', 'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.05', 'audio_encoding': 'AAC', 'audio_bitrate': '24'},
]

def parse_video_info(raw_info):
    """Parser for YouTube's get_video_info data.
    Returns a dict, where 'url_encoded_fmt_stream_map' maps to a sorted list.
    """
    
    # Percent-encoding reserved characters, used as separators.
    sepr = {
        '&': '%26',
        ',': '%2C',
        '=': '%3D',
    }
    
    # fmt_level = {'itag': level, ...}
    # itag of a higher quality maps to a lower level number.
    # The highest quality has level number 0.
    fmt_level = dict(
        zip(
            [str(codec['itag'])
                for codec in
                    youtube_codecs],
            range(len(youtube_codecs))))
    
    # {key1: value1, key2: value2, ...,
    #   'url_encoded_fmt_stream_map': [{'itag': '38', ...}, ...]
    # }
    return dict(
        [(lambda metadata:
            ['url_encoded_fmt_stream_map', (
                lambda stream_map:
                    sorted(
                        [dict(
                            [subitem.split(sepr['='])
                                for subitem in
                                    item.split(sepr['&'])])
                            for item in
                                stream_map.split(sepr[','])],
                        key =
                            lambda stream:
                                fmt_level[stream['itag']]))
                (metadata[1])]
            if metadata[0] == 'url_encoded_fmt_stream_map'
            else metadata)
        (item.split('='))
            for item in
                raw_info.split('&')])

# Signature decryption algorithm, reused code from youtube-dl
def decrypt_signature(s):
    if len(s) == 88:
        return s[48] + s[81:67:-1] + s[82] + s[66:62:-1] + s[85] + s[61:48:-1] + s[67] + s[47:12:-1] + s[3] + s[11:3:-1] + s[2] + s[12]
    elif len(s) == 87:
        return s[62] + s[82:62:-1] + s[83] + s[61:52:-1] + s[0] + s[51:2:-1]
    elif len(s) == 86:
        return s[2:63] + s[82] + s[64:82] + s[63]
    elif len(s) == 85:
        return s[76] + s[82:76:-1] + s[83] + s[75:60:-1] + s[0] + s[59:50:-1] + s[1] + s[49:2:-1]
    elif len(s) == 84:
        return s[83:36:-1] + s[2] + s[35:26:-1] + s[3] + s[25:3:-1] + s[26]
    elif len(s) == 83:
        return s[52] + s[81:55:-1] + s[2] + s[54:52:-1] + s[82] + s[51:36:-1] + s[55] + s[35:2:-1] + s[36]
    elif len(s) == 82:
        return s[36] + s[79:67:-1] + s[81] + s[66:40:-1] + s[33] + s[39:36:-1] + s[40] + s[35] + s[0] + s[67] + s[32:0:-1] + s[34]
    else:
        raise Exception('Unable to decrypt signature, key length %d not supported; retrying might work' % (len(s)))

def youtube_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    
    raw_info = request.urlopen('http://www.youtube.com/get_video_info?video_id=%s' % id).read().decode('utf-8')
    
    video_info = parse_video_info(raw_info)
    
    if video_info['status'] == 'ok' and not video_info['use_cipher_signature'] == 'True': # use get_video_info data
        
        title = parse.unquote(video_info['title'].replace('+', ' '))
        
        signature = video_info['url_encoded_fmt_stream_map'][0]['sig']
        url = parse.unquote(parse.unquote(video_info['url_encoded_fmt_stream_map'][0]['url'])) + "&signature=%s" % signature
        
    else: # parse video page when "embedding disabled by request"
        
        import json
        html = request.urlopen('http://www.youtube.com/watch?v=' + id).read().decode('utf-8')
        html = unescape_html(html)
        yt_player_config = json.loads(r1(r'ytplayer.config = ([^\n]+);', html))
        title = yt_player_config['args']['title']
        title = unicodize(title)
        title = parse.unquote(title)
        title = escape_file_path(title)
        
        for itag in [
            '38',
            '46', '37',
            '102', '45', '22',
            '84',
            '120',
            '85',
            '44', '35',
            '101', '100', '43', '34', '82', '18',
            '6', '83', '13', '5', '36', '17',
        ]:
            fmt = r1(r'([^,\"]*itag=' + itag + "[^,\"]*)", html)
            if fmt:
                url = r1(r'url=([^\\]+)', fmt)
                url = unicodize(url)
                url = parse.unquote(url)
                sig = r1(r'sig=([^\\]+)', fmt) or decrypt_signature(r1(r's=([^\\]+)', fmt))
                url = url + '&signature=' + sig
                break
        try:
            url
        except NameError:
            url = r1(r'ytdns.ping\("([^"]+)"[^;]*;</script>', html)
            url = unicodize(url)
            url = re.sub(r'\\/', '/', url)
            url = re.sub(r'generate_204', 'videoplayback', url)
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def youtube_download(url, output_dir = '.', merge = True, info_only = False):
    id = r1(r'youtu.be/(.*)', url)
    if not id:
        id = parse.parse_qs(parse.urlparse(url).query)['v'][0]
    assert id
    
    youtube_download_by_id(id, None, output_dir, merge = merge, info_only = info_only)

site_info = "YouTube.com"
download = youtube_download
download_playlist = playlist_not_supported('youtube')
