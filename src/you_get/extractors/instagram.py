#!/usr/bin/env python

__all__ = ['instagram_download']

from ..common import *

def instagram_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.2592.87',
        'sec-fetch-mode': 'navigate'  # important
    }

    url = r1(r'([^?]*)', url)
    cont = get_content(url, headers=headers)

    vid = r1(r'instagram.com/\w+/([^/]+)', url)
    description = r1(r'<meta property="og:title" content="([^"]*)"', cont) or \
        r1(r'<title>([^<]*)</title>', cont) # with logged-in cookies
    title = "{} [{}]".format(description.replace("\n", " "), vid)

    appId = r1(r'"appId":"(\d+)"', cont)
    media_id = r1(r'"media_id":"(\d+)"', cont)
    logging.debug('appId: %s' % appId)
    logging.debug('media_id: %s' % media_id)

    api_url = 'https://i.instagram.com/api/v1/media/%s/info/' % media_id
    try:
        api_cont = get_content(api_url, headers={**fake_headers, **{'x-ig-app-id': appId}})
        post = json.loads(api_cont)
    except:
        log.wtf('[Error] Please specify a cookie file.')

    for item in post['items']:
        code = item['code']
        carousel_media = item.get('carousel_media') or [item]
        for i, media in enumerate(carousel_media):
            title = '%s [%s]' % (code, i)
            image_url = media['image_versions2']['candidates'][0]['url']
            ext = image_url.split('?')[0].split('.')[-1]
            size = int(get_head(image_url)['Content-Length'])

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls=[image_url],
                              title=title,
                              ext=ext,
                              total_size=size,
                              output_dir=output_dir)

            # download videos (if any)
            if 'video_versions' in media:
                video_url = media['video_versions'][0]['url']
                ext = video_url.split('?')[0].split('.')[-1]
                size = int(get_head(video_url)['Content-Length'])

                print_info(site_info, title, ext, size)
                if not info_only:
                    download_urls(urls=[video_url],
                                  title=title,
                                  ext=ext,
                                  total_size=size,
                                  output_dir=output_dir)

site_info = "Instagram.com"
download = instagram_download
download_playlist = playlist_not_supported('instagram')
