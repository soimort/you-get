#!/usr/bin/env python

__all__ = ['darkibox_download']

from ..common import *
import re


def _unpack_js(packed):
    """Unpack Dean Edwards' packed JavaScript.

    Handles eval(function(p,a,c,k,e,d){...}) patterns.
    """
    # Extract the arguments to the inner function
    m = re.search(
        r"eval\(function\(p,a,c,k,e,[dr]\)\{.*?\}\('(.+)',(\d+),(\d+),'([^']+)'",
        packed, re.DOTALL
    )
    if not m:
        return packed
    payload, radix, count, keywords = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).split('|')

    def _base_n(num, base):
        digits = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if num < 0:
            return '-' + _base_n(-num, base)
        result = ''
        while num:
            result = digits[num % base] + result
            num //= base
        return result or '0'

    def _lookup(match):
        word = match.group(0)
        n = _base_n(int(word, 36), radix) if radix <= 36 else word
        try:
            idx = int(word, 36)
        except ValueError:
            idx = int(word)
        return keywords[idx] if idx < len(keywords) and keywords[idx] else word

    # Replace each word token with its keyword
    unpacked = re.sub(r'\b\w+\b', _lookup, payload)
    return unpacked


def _extract_file_code(url):
    """Extract the file code from various darkibox URL patterns.

    Supports:
        darkibox.com/FILECODE
        darkibox.com/d/FILECODE
        darkibox.com/embed-FILECODE.html
    """
    file_code = match1(url, r'darkibox\.com/embed-([a-zA-Z0-9]+)') or \
                match1(url, r'darkibox\.com/d/([a-zA-Z0-9]+)') or \
                match1(url, r'darkibox\.com/([a-zA-Z0-9]+)')
    return file_code


def darkibox_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Download videos from darkibox.com."""

    file_code = _extract_file_code(url)
    if not file_code:
        raise ValueError('Cannot extract file code from URL: ' + url)

    embed_url = 'https://darkibox.com/embed-{}.html'.format(file_code)

    # GET the embed page first (sets cookies, gets any tokens)
    embed_page = get_content(embed_url)
    title = match1(embed_page, r'<title>([^<]+)</title>') or file_code
    # Clean up title
    title = title.replace(' - DarkiBox', '').strip()
    if not title:
        title = file_code

    # POST to the download endpoint
    post_data = {
        'op': 'embed',
        'file_code': file_code,
        'auto': '1',
    }
    response = post_content(
        'https://darkibox.com/dl',
        post_data=post_data,
        headers={'Referer': embed_url}
    )

    # Response contains packed JS; unpack it
    unpacked = _unpack_js(response)

    # Extract video URL from the unpacked JS
    # PlayerJS format: file:"URL"
    video_url = match1(unpacked, r'file:\s*"([^"]+)"') or \
                match1(unpacked, r'src:\s*"([^"]+)"') or \
                match1(unpacked, r'"file"\s*:\s*"([^"]+)"')

    if not video_url:
        raise ValueError('Cannot extract video URL from darkibox response')

    mime, ext, size = url_info(video_url, headers={'Referer': embed_url})

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls(
            [video_url], title, ext, size,
            output_dir=output_dir, merge=merge,
            headers={'Referer': embed_url}
        )


site_info = "DarkiBox"
download = darkibox_download
download_playlist = playlist_not_supported('darkibox')
