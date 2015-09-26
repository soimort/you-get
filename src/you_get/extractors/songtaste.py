#!/usr/bin/env python

__all__ = ['songtaste_download']

from ..common import *
import urllib.error

def songtaste_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://www.songtaste.com/song/\d+', url):
        old_fake_headers = fake_headers
        id = r1(r'http://www.songtaste.com/song/(\d+)', url)
        player_url = 'http://www.songtaste.com/playmusic.php?song_id='+str(id)
        fake_headers['Referer'] = player_url
        html = get_response(player_url).data
        r = '''^WrtSongLine\((.*)\)'''
        
        reg = re.compile(r , re.M)
        
        m = reg.findall(html.decode('gbk'))
        l = m[0].replace('"', '').replace(' ', '').split(',')
        
        title = l[2] + '-' + l[1]
        
        for i in range(0, 10):
            real_url = l[5].replace('http://mg', 'http://m%d' % i)
            try:
                type, ext, size = url_info(real_url, True)
            except urllib.error.HTTPError as e:
                if 403 == e.code:
                    continue
                else:
                    raise e
            break
        
        print_info(site_info, title, type, size)
        
        if not info_only:
            download_urls([real_url], title, ext, size, output_dir, refer = url, merge = merge, faker = True)
        fake_hreaders = old_fake_headers

site_info = "SongTaste.com"
download = songtaste_download
download_playlist = playlist_not_supported('songtaste')
