#!/usr/bin/env python

__all__ = ['universal_download']

from ..common import *
from .embed import *

def universal_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    try:
        content_type = get_head(url, headers=fake_headers)['Content-Type']
    except:
        content_type = get_head(url, headers=fake_headers, get_method='GET')['Content-Type']
    if content_type.startswith('text/html'):
        try:
            embed_download(url, output_dir, merge=merge, info_only=info_only)
        except: pass
        else: return

    domains = url.split('/')[2].split('.')
    if len(domains) > 2: domains = domains[1:]
    site_info = '.'.join(domains)

    if content_type.startswith('text/html'):
        # extract an HTML page
        response = get_response(url, faker=True)
        page = str(response.data)

        page_title = r1(r'<title>([^<]*)', page)
        if page_title:
            page_title = unescape_html(page_title)

        # most common media file extensions on the Internet
        media_exts = ['\.flv', '\.mp3', '\.mp4', '\.webm',
                      '[-_]1\d\d\d\.jpe?g', '[-_][6-9]\d\d\.jpe?g', # tumblr
                      '[-_]1\d\d\dx[6-9]\d\d\.jpe?g',
                      '[-_][6-9]\d\dx1\d\d\d\.jpe?g',
                      '[-_][6-9]\d\dx[6-9]\d\d\.jpe?g',
                      's1600/[\w%]+\.jpe?g', # blogger
                      'img[6-9]\d\d/[\w%]+\.jpe?g' # oricon?
        ]

        urls = []
        for i in media_exts:
            urls += re.findall(r'(https?://[^;"\'\\]+' + i + r'[^;"\'\\]*)', page)

            p_urls = re.findall(r'(https?%3A%2F%2F[^;&]+' + i + r'[^;&]*)', page)
            urls += [parse.unquote(url) for url in p_urls]

            q_urls = re.findall(r'(https?:\\\\/\\\\/[^;"\']+' + i + r'[^;"\']*)', page)
            urls += [url.replace('\\\\/', '/') for url in q_urls]

        # a link href to an image is often an interesting one
        urls += re.findall(r'href="(https?://[^"]+\.jpe?g)"', page)
        urls += re.findall(r'href="(https?://[^"]+\.png)"', page)
        urls += re.findall(r'href="(https?://[^"]+\.gif)"', page)

        # have some candy!
        candies = []
        i = 1
        for url in set(urls):
            filename = parse.unquote(url.split('/')[-1])
            if 5 <= len(filename) <= 80:
                title = '.'.join(filename.split('.')[:-1])
            else:
                title = '%s' % i
                i += 1

            candies.append({'url': url,
                            'title': title})

        for candy in candies:
            try:
                mime, ext, size = url_info(candy['url'], faker=True)
                if not size: size = float('Int')
            except:
                continue
            else:
                print_info(site_info, candy['title'], ext, size)
                if not info_only:
                    download_urls([candy['url']], candy['title'], ext, size,
                                  output_dir=output_dir, merge=merge,
                                  faker=True)
        return

    else:
        # direct download
        filename = parse.unquote(url.split('/')[-1])
        title = '.'.join(filename.split('.')[:-1])
        ext = filename.split('.')[-1]
        _, _, size = url_info(url, faker=True)
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([url], title, ext, size,
                          output_dir=output_dir, merge=merge,
                          faker=True)
        return

site_info = None
download = universal_download
download_playlist = playlist_not_supported('universal')
