#!/usr/bin/env python

__all__ = ['qq_download']

from you_get.common import *
import uuid, urllib
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


def qq_download_by_id(id, title=None, output_dir='.', merge=True, info_only=False, urls_only=False):
    data = {'vids': id, 'otype': 'json'}
    url = urllib.request.Request('http://vv.video.qq.com/getinfo', urllib.parse.urlencode(data).encode('utf-8'))
    f = urllib.request.urlopen(url)
    json_str = f.read()
    data = json.loads(json_str[13:-1].decode('utf-8'))
    format_id = 10202
    file_id = 1
    for format_info in data['fl']['fi']:
        if format_info['sl'] > 0:
            format_id = format_info['id']
            file_id = format_info['sl']
            break
    file_name = data['vl']['vi'][0]['fn']
    split_pos = file_name.rfind('.')
    file_name = file_name[:split_pos] + '.%d' % file_id + file_name[split_pos:]
    video_urls = [ui['url'] for ui in data['vl']['vi'][0]['ul']['ui']]

    data = {'format': format_id, 'otype': 'json', 'vid': id, 'filename': file_name}
    url = urllib.request.Request('http://vv.video.qq.com/getkey', urllib.parse.urlencode(data).encode('utf-8'))
    f = urllib.request.urlopen(url)
    json_str = f.read()
    data = json.loads(json_str[13:-1].decode('utf-8'))
    video_key = data['key']

    urls = []
    size = 0
    ext = ''
    for url in video_urls:
        try:
            url = "%s%s?vkey=%s" % (url, file_name, video_key)
            _, ext, size = url_info(url)
            urls = [url]
            break
        except:
            print(url)

    if urls_only:
        return urls, size, ext, {}

    if not info_only:
        download_urls([url], title, 'flv', size, output_dir = output_dir, merge = merge)

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


if __name__ == '__main__':
    #print(qq_download('http://v.qq.com/cover/c/crfns95chw1snp2/t0012q2nz5m.html', urls_only = True))
    # print(get_videoId('http://v.qq.com/cover/k/kuegopa6s70qeu1.html?vid=t0013jyqbo7'))
    print(qq_download_by_id('u001428c4av', urls_only=True))