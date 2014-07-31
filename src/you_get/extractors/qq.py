#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *

#QQMUSIC
#SINGLE
#1. http://y.qq.com/#type=song&mid=000A9lMb0iEqwN
#2. http://y.qq.com/#type=song&id=4754713
#3. http://s.plcloud.music.qq.com/fcgi-bin/fcg_yqq_song_detail_info.fcg?songmid=002NqCeX3owQIw
#4. http://s.plcloud.music.qq.com/fcgi-bin/fcg_yqq_song_detail_info.fcg?songid=4754713
#ALBUM
#1. http://y.qq.com/y/static/album/3/c/00385vBa0n3O3c.html?pgv_ref=qqmusic.y.index.music.pic1
#2. http://y.qq.com/#type=album&mid=004c62RC2uujor
#MV
#can download as video through qq_download_by_id
#1. http://y.qq.com/y/static/mv/mv_play.html?vid=i0014ufczcw

def qq_download_by_id(id, title=None, output_dir='.', merge=True, info_only=False):
    xml = get_html('http://www.acfun.tv/getinfo?vids=%s' % id)
    from xml.dom.minidom import parseString
    doc = parseString(xml)
    doc_root = doc.getElementsByTagName('root')[0]
    doc_vl = doc_root.getElementsByTagName('vl')[0]
    doc_vi = doc_vl.getElementsByTagName('vi')[0]
    fn = doc_vi.getElementsByTagName('fn')[0].firstChild.data
    fclip = doc_vi.getElementsByTagName('fclip')[0].firstChild.data
    if int(fclip) > 0:
        fn = fn[:-4] + "." + fclip + fn[-4:]
    fvkey = doc_vi.getElementsByTagName('fvkey')[0].firstChild.data
    doc_ul = doc_vi.getElementsByTagName('ul')
    url = doc_ul[0].getElementsByTagName('url')[0].firstChild.data
    url = url + fn + '?vkey=' + fvkey

    _, ext, size = url_info(url)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir = '.', merge = True, info_only = False):
    if re.match(r'http://v.qq.com/([^\?]+)\?vid', url):
        aid = r1(r'(.*)\.html', url)
        vid = r1(r'http://v.qq.com/[^\?]+\?vid=(\w+)', url)
        url = 'http://sns.video.qq.com/tvideo/fcgi-bin/video?vid=%s' % vid

    if re.match(r'http://y.qq.com/([^\?]+)\?vid', url):
        vid = r1(r'http://y.qq.com/[^\?]+\?vid=(\w+)', url)

        url = "http://v.qq.com/page/%s.html" % vid

        r_url = r1(r'<meta http-equiv="refresh" content="0;url=([^"]*)', get_html(url))
        if r_url:
            aid = r1(r'(.*)\.html', r_url)
            url = "%s/%s.html" % (aid, vid)

    if re.match(r'http://static.video.qq.com/.*vid=', url):
        vid = r1(r'http://static.video.qq.com/.*vid=(\w+)', url)
        url = "http://v.qq.com/page/%s.html" % vid

    if re.match(r'http://v.qq.com/cover/.*\.html', url):
        html = get_html(url)
        vid = r1(r'vid:"([^"]+)"', html)
        url = 'http://sns.video.qq.com/tvideo/fcgi-bin/video?vid=%s' % vid

    html = get_html(url)

    title = match1(html, r'<title>(.+?)</title>', r'title:"([^"]+)"')[0].strip()
    assert title
    title = unescape_html(title)
    title = escape_file_path(title)

    try:
        id = vid
    except:
        id = r1(r'vid:"([^"]+)"', html)

    qq_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
