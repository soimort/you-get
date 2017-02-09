#!/usr/bin/env python

__all__ = ['nicovideo_download']

from ..common import *

def nicovideo_login(user, password):
    post_data = {
        'mail_tel': user,
        'password': password,
    }
    response = request.urlopen(request.Request(
        'https://account.nicovideo.jp/api/v1/login?site=niconico',
        headers=fake_headers,
        data=parse.urlencode(post_data).encode('utf-8'),
    ))
    return response.headers

def nicovideo_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    import ssl
    ssl_context = request.HTTPSHandler(
context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    cookie_handler = request.HTTPCookieProcessor()
    opener = request.build_opener(ssl_context, cookie_handler)
    request.install_opener(opener)

    import netrc, getpass
    try:
        info = netrc.netrc().authenticators('nicovideo')
    except:
        info = None
    if info is None:
        user = input("Email/Tel: ")
        password = getpass.getpass("Password: ")
    else:
        user, password = info[0], info[2]
    print("Logging in...")
    nicovideo_login(user, password)

    html = get_content(url)
    # There are two possible layouts where titles are embedded differently.
    # See https://gist.github.com/ed95394afc6eff8a781395ac5afcbe48 for sample HTML pages.
    try:
        title = unicodize(r1(r'<h1 [^>]*class="txt-title"[^>]*>([^<]+)</h1>', html))
    except TypeError:
        title = unicodize(r1(r'<span [^>]*class="videoHeaderTitle"[^>]*>([^<]+)</span>', html))

    vid = url.split('/')[-1].split('?')[0]
    api_html = get_content('http://flapi.nicovideo.jp/api/getflv?v=%s' % vid)
    real_url = parse.unquote(r1(r'url=([^&]+)&', api_html))

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Nicovideo.jp"
download = nicovideo_download
download_playlist = playlist_not_supported('nicovideo')
