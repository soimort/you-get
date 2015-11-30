#!/usr/bin/env python

__all__ = ['veoh_download']

from ..common import *
import urllib.error

def veoh_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Get item_id'''
    if re.match(r'http://www.veoh.com/watch/\w+', url):
        item_id = match1(url, r'http://www.veoh.com/watch/(\w+)')
    elif re.match(r'http://www.veoh.com/m/watch.php\?v=\.*', url):
        item_id = match1(url, r'http://www.veoh.com/m/watch.php\?v=(\w+)')
    else:
        raise NotImplementedError('Cannot find item ID')
    veoh_download_by_id(item_id, output_dir = '.', merge = False, info_only = info_only, **kwargs)

#----------------------------------------------------------------------
def veoh_download_by_id(item_id, output_dir = '.', merge = False, info_only = False, **kwargs):
    """Source: Android mobile"""
    webpage_url = 'http://www.veoh.com/m/watch.php?v={item_id}&quality=1'.format(item_id = item_id)

    #grab download URL
    a = get_content(webpage_url, decoded=True)
    url = match1(a, r'<source src="(.*?)\"\W')

    #grab title
    title = match1(a, r'<meta property="og:title" content="([^"]*)"')

    type_, ext, size = url_info(url)
    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)


site_info = "Veoh"
download = veoh_download
download_playlist = playlist_not_supported('veoh')
