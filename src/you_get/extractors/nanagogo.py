#!/usr/bin/env python

__all__ = ['nanagogo_download']

from ..common import *

def nanagogo_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    title = r1(r'<meta property="og:title" content="([^"]*)"', html)
    postId = r1(r'postId\s*:\s*"([^"]*)"', html)
    title += ' - ' + postId
    try: # extract direct video
        source = r1(r'<meta property="og:video" content="([^"]*)"', html)
        mime, ext, size = url_info(source)

        print_info(site_info, title, mime, size)
        if not info_only:
            download_urls([source], title, ext, size, output_dir, merge=merge)

    except: # official API
        talkId = r1(r'talkId\s*:\s*"([^"]*)"', html)
        apiUrl = 'http://7gogo.jp/api/talk/post/detail/%s/%s' % (talkId, postId)
        info = json.loads(get_content(apiUrl))
        images = []
        for post in info['posts']:
            for item in post['body']:
                if 'movieUrlHq' in item:
                    url = item['movieUrlHq']
                    name = title
                    _, ext, size = url_info(url)
                    images.append({'title': name,
                                   'url': url,
                                   'ext': ext,
                                   'size': size})

                elif 'image' in item:
                    url = item['image']
                    name = title
                    #filename = parse.unquote(url.split('/')[-1])
                    #name = '.'.join(filename.split('.')[:-1])
                    #ext = filename.split('.')[-1]
                    #size = int(get_head(url)['Content-Length'])
                    _, ext, size = url_info(url)
                    images.append({'title': name,
                                   'url': url,
                                   'ext': ext,
                                   'size': size})

        size = sum([i['size'] for i in images])
        print_info(site_info, title, ext, size)

        if not info_only:
            for i in images:
                title = i['title']
                ext = i['ext']
                size = i['size']
                url = i['url']
                print_info(site_info, title, ext, size)
                download_urls([url], title, ext, size,
                              output_dir=output_dir)

site_info = "7gogo.jp"
download = nanagogo_download
download_playlist = playlist_not_supported('nanagogo')
