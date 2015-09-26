#!/usr/bin/env python

__all__ = ['nicovideo_download']

from ..common import *

def nicovideo_login(user, password):
    data = "current_form=login&mail=" + user +"&password=" + password + "&login_submit=Log+In"
    response = request.urlopen(request.Request("https://secure.nicovideo.jp/secure/login?site=niconico", headers=fake_headers, data=data.encode('utf-8')))
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
    except FileNotFoundError:
        info = None
    if info is None:
        user = input("User:     ")
        password = getpass.getpass("Password: ")
    else:
        user, password = info[0], info[2]
    print("Logging in...")
    nicovideo_login(user, password)

    html = get_html(url) # necessary!
    title = unicodize(r1(r'<span class="videoHeaderTitle"[^>]*>([^<]+)</span>', html))

    vid = url.split('/')[-1].split('?')[0]
    api_html = get_html('http://www.nicovideo.jp/api/getflv?v=%s' % vid)
    real_url = parse.unquote(r1(r'url=([^&]+)&', api_html))

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Nicovideo.jp"
download = nicovideo_download
download_playlist = playlist_not_supported('nicovideo')
