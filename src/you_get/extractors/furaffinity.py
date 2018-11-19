#!/usr/bin/env python

__all__ = ['furaffinity_download', 'furaffinity_download_playlist']

from ..common import *

# check url
def gallery_page(url):
    return re.search(r'furaffinity.net/gallery', url)

def scripts_page(url):
    return re.search(r'furaffinity.net/scripts', url)

def favorites_page(url):
    return re.search(r'furaffinity.net/favorites', url)

def view_page(url):
    return re.search(r'furaffinity.net/view', url)

# check html
def check(html):
    if re.search(r'has elected to make their content available to registered users only', html):
        print('Please use --cookie to access this page.')
        exit(0)
    elif re.search(r'The username "\w+" could not be found', html):
        print('This username cannot be found.')
        exit(0)
    elif re.search(r'There are no submissions to list', html):
        print('There are no submissions to list.')
        exit(0)

def not_supported():
    print('There\'s nothing to download.')
    print('You can try some other page url like gallery, scripts, favorites or view page.')
    exit(0)

def furaffinity_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if gallery_page(url) or scripts_page(url) or favorites_page(url):
        print('This page contains a list of picture, use --playlist to download all.')
        exit(0)

    if not view_page(url):
        not_supported()

    html = get_html(url, faker=True)
    check(html)

    fileurl   = 'http:' + r1(r'<a href="(.*)">Download', html)
    parseurl  = parse.quote(fileurl, ';/?:@&=+$,', encoding='utf-8')
    filetitle = r1(r'<title>(.+) by', html)
    filename  = r1(r'([^/]+)$', fileurl)
    filetype  = r1(r'([^.]+)$', filename)
    filesize  = int(get_head(parseurl)['Content-Length'])

    print_info(site_info, filetitle, filetype, filesize)
    download_urls([parseurl], filename, filetype, filesize, output_dir=output_dir)

def furaffinity_download_playlist(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if view_page(url):
        furaffinity_download(url, output_dir=output_dir, merge=merge, info_only=info_only)

    elif not (gallery_page(url) or scripts_page(url) or favorites_page(url)):
        not_supported()

    else:
        html = get_html(url, faker=True)
        check(html)

        urls = re.findall(r'<a href="(/view/\d+)/" ', html)
        if not urls:
            print('This page has nothing to download.')
            exit(0)

        for i in range(0, len(urls)):
            print('[{0} of {1}]'.format(i+1, len(urls)))
            url = 'http://www.furaffinity.net' + urls[i]
            furaffinity_download(url, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "furaffinity.net"
download = furaffinity_download
download_playlist = furaffinity_download_playlist
