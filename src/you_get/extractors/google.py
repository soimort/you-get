#!/usr/bin/env python

__all__ = ['google_download']

from ..common import *

import re

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
fmt_level = dict(
    zip(
        [str(codec['itag'])
            for codec in
                youtube_codecs],
        range(len(youtube_codecs))))

def google_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe = ':/+%?=')

    service = url.split('/')[2].split('.')[0]

    if service == 'plus': # Google Plus

        if not re.search(r'plus.google.com/photos/[^/]*/albums/\d+/\d+', url):
            html = get_html(parse.unquote(url))
            url = "https://plus.google.com/" + r1(r'"(photos/\d+/albums/\d+/\d+)', html)
            title = r1(r'<title>([^<\n]+)', html)
        else:
            title = None

        html = get_html(url)
        temp = re.findall(r'\[(\d+),\d+,\d+,"([^"]+)"\]', html)
        temp = sorted(temp, key = lambda x : fmt_level[x[0]])
        real_urls = [unicodize(i[1]) for i in temp if i[0] == temp[0][0]]

        if title is None:
            post_url = r1(r'"(https://plus.google.com/[^/]+/posts/[^"]*)"', html)
            post_author = r1(r'/\+([^/]+)/posts', post_url)
            if post_author:
                post_url = "https://plus.google.com/+%s/posts/%s" % (parse.quote(post_author), r1(r'posts/(.+)', post_url))
            post_html = get_html(post_url)
            title = r1(r'<title[^>]*>([^<\n]+)', post_html)

        if title is None:
            response = request.urlopen(request.Request(real_url))
            if response.headers['content-disposition']:
                filename = parse.unquote(r1(r'filename="?(.+)"?', response.headers['content-disposition'])).split('.')
                title = ''.join(filename[:-1])

        if not real_urls:
            # extract the image
            # FIXME: download multple images / albums
            real_urls = [r1(r'<meta property="og:image" content="([^"]+)', html)]
            post_date = r1(r'"(20\d\d-[01]\d-[0123]\d)"', html)
            post_id = r1(r'/posts/([^"]+)', html)
            title = post_date + "_" + post_id

        for (i, real_url) in enumerate(real_urls):
            title_i = "%s[%s]" % (title, i) if len(real_urls) > 1 else title
            type, ext, size = url_info(real_url)
            if ext is None:
                ext = 'mp4'

            print_info(site_info, title_i, ext, size)
            if not info_only:
                download_urls([real_url], title_i, ext, size, output_dir, merge = merge)

    elif service in ['docs', 'drive'] : # Google Docs

        html = get_html(url)

        title = r1(r'"title":"([^"]*)"', html) or r1(r'<meta itemprop="name" content="([^"]*)"', html)
        if len(title.split('.')) > 1:
            title = ".".join(title.split('.')[:-1])

        docid = r1(r'"docid":"([^"]*)"', html)

        request.install_opener(request.build_opener(request.HTTPCookieProcessor()))

        request.urlopen(request.Request("https://docs.google.com/uc?id=%s&export=download" % docid))
        real_url ="https://docs.google.com/uc?export=download&confirm=no_antivirus&id=%s" % docid

        type, ext, size = url_info(real_url)

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Google.com"
download = google_download
download_playlist = playlist_not_supported('google')
