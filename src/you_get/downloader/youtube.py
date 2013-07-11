#!/usr/bin/env python

__all__ = ['youtube_download', 'youtube_download_by_id']

from ..common import *

# YouTube media encoding options, in descending quality order.
# taken from http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs, 3/22/2013.
yt_codecs = [
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
        return s[:81]
    elif len(s) == 82:
        return s[36] + s[79:67:-1] + s[81] + s[66:40:-1] + s[33] + s[39:36:-1] + s[40] + s[35] + s[0] + s[67] + s[32:0:-1] + s[34]
    else:
        raise Exception('Unable to decrypt signature, key length %d not supported; retrying might work' % (len(s)))

def youtube_download_by_id(id, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a YouTube video by its unique id.
    """
    
    raw_video_info = get_content('http://www.youtube.com/get_video_info?video_id=%s' % id)
    video_info = parse.parse_qs(raw_video_info)
    
    if video_info['status'] == ['ok'] and ('use_cipher_signature' not in video_info or video_info['use_cipher_signature'] == ['False']):
        title = parse.unquote_plus(video_info['title'][0])
        stream_list = parse.parse_qs(raw_video_info)['url_encoded_fmt_stream_map'][0].split(',')
        
    else:
        # Parse video page when video_info is not usable.
        video_page = get_content('http://www.youtube.com/watch?v=%s' % id)
        ytplayer_config = json.loads(match1(video_page, r'ytplayer.config\s*=\s*([^\n]+);'))
        
        title = ytplayer_config['args']['title']
        stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')
    
    streams = {
        parse.parse_qs(stream)['itag'][0] : parse.parse_qs(stream)
            for stream in stream_list
    }
    
    for codec in yt_codecs:
        itag = str(codec['itag'])
        if itag in streams:
            download_stream = streams[itag]
            break
    
    url = download_stream['url'][0]
    if 'sig' in download_stream:
        sig = download_stream['sig'][0]
    else:
        sig = decrypt_signature(download_stream['s'][0])
    url = '%s&signature=%s' % (url, sig)
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def youtube_download(url, output_dir='.', merge=True, info_only=False):
    """Downloads YouTube videos by URL.
    """
    
    id = match1(url, r'youtu.be/([^/]+)') or parse_query_param(url, 'v')
    assert id
    
    youtube_download_by_id(id, title=None, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "YouTube.com"
download = youtube_download
download_playlist = playlist_not_supported('youtube')
