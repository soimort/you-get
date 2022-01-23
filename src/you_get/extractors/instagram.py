#!/usr/bin/env python

__all__ = ['instagram_download']

from ..common import *

def instagram_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    url = r1(r'([^?]*)', url)
    cont = get_content(url, headers=fake_headers)

    vid = r1(r'instagram.com/\w+/([^/]+)', url)
    description = r1(r'<meta property="og:title" content="([^"]*)"', cont) or \
        r1(r'<title>\s([^<]*)</title>', cont) # with logged-in cookies
    title = "{} [{}]".format(description.replace("\n", " "), vid)

    stream = r1(r'<meta property="og:video" content="([^"]*)"', cont)
    if stream:
        _, ext, size = url_info(stream)

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([stream], title, ext, size, output_dir, merge=merge)
    else:
        data = re.search(r'window\._sharedData\s*=\s*(.*);</script>', cont)
        try:
            info = json.loads(data.group(1))
            post = info['entry_data']['PostPage'][0]
            assert post
        except:
            # with logged-in cookies
            data = re.search(r'window\.__additionalDataLoaded\(\'[^\']+\',(.*)\);</script>', cont)
            if data is not None:
                log.e('[Warning] Cookies needed.')
            post = json.loads(data.group(1))

        if 'edge_sidecar_to_children' in post['graphql']['shortcode_media']:
            edges = post['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
            for edge in edges:
                title = edge['node']['shortcode']
                image_url = edge['node']['display_url']
                if 'video_url' in edge['node']:
                    image_url = edge['node']['video_url']
                ext = image_url.split('?')[0].split('.')[-1]
                size = int(get_head(image_url)['Content-Length'])

                print_info(site_info, title, ext, size)
                if not info_only:
                    download_urls(urls=[image_url],
                                  title=title,
                                  ext=ext,
                                  total_size=size,
                                  output_dir=output_dir)
        else:
            title = post['graphql']['shortcode_media']['shortcode']
            image_url = post['graphql']['shortcode_media']['display_url']
            if 'video_url' in post['graphql']['shortcode_media']:
                image_url = post['graphql']['shortcode_media']['video_url']
            ext = image_url.split('?')[0].split('.')[-1]
            size = int(get_head(image_url)['Content-Length'])

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls=[image_url],
                              title=title,
                              ext=ext,
                              total_size=size,
                              output_dir=output_dir)

site_info = "Instagram.com"
download = instagram_download
download_playlist = playlist_not_supported('instagram')
