#!/usr/bin/env python

__all__ = ['nicovideo_download']

from ..common import *

def nicovideo_login(user, password):
    data = "current_form=login&mail=" + user +"&password=" + password + "&login_submit=Log+In"
    response = request.urlopen(request.Request("https://secure.nicovideo.jp/secure/login?site=niconico", headers = fake_headers, data = data.encode('utf-8')))
    return response.headers

def nicovideo_download(url, output_dir = '.', merge = True, info_only = False):
    request.install_opener(request.build_opener(request.HTTPCookieProcessor()))
    
    import netrc, getpass
    info = netrc.netrc().authenticators('nicovideo')
    if info is None:
        user = input("User:     ")
        password = getpass.getpass("Password: ")
    else:
        user, password = info[0], info[2]
    print("Logging in...")
    nicovideo_login(user, password)
    
    html = get_html(url) # necessary!
    title = unicodize(r1(r'title:\s*\'(.*)\',', html))
    
    api_html = get_html('http://www.nicovideo.jp/api/getflv?v=%s' % url.split('/')[-1])
    real_url = parse.unquote(r1(r'url=([^&]+)&', api_html))
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Nicovideo.jp"
download = nicovideo_download
download_playlist = playlist_not_supported('nicovideo')
