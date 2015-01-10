#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *
<<<<<<< HEAD
import uuid
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
    # fclip = doc_vi.getElementsByTagName('fclip')[0].firstChild.data
    # fc=doc_vi.getElementsByTagName('fc')[0].firstChild.data
    fvkey = doc_vi.getElementsByTagName('fvkey')[0].firstChild.data
    doc_ul = doc_vi.getElementsByTagName('ul')


    url = doc_ul[0].getElementsByTagName('url')[1].firstChild.data

    # print(i.firstChild.data)
    urls=[]
    ext=fn[-3:]
    size=0
    for i in doc.getElementsByTagName("cs"):
        size+=int(i.firstChild.data)

    # size=sum(map(int,doc.getElementsByTagName("cs")))
    locid=str(uuid.uuid4())
    for i in doc.getElementsByTagName("ci"):
        urls.append(url+fn[:-4] + "." + i.getElementsByTagName("idx")[0].firstChild.data + fn[-4:] + '?vkey=' + fvkey+ '&sdtfrom=v1000&type='+ fn[-3:0] +'&locid=' + locid + "&&level=1&platform=11&br=133&fmt=hd&sp=0")

    # if int(fclip) > 0:
    #     fn = fn[:-4] + "." + fclip + fn[-4:]
    # url = url + fn + '?vkey=' + fvkey

    # _, ext, size = url_info(url)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir = '.', merge = True, info_only = False):
<<<<<<< HEAD
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
=======
    content = get_html(url)
    video_info = to_dict(match1(content, r'var\s+VIDEO_INFO\s?=\s?({[^}]+})'))
    vid = video_info['vid']
    title = video_info['title']
>>>>>>> 20fe47f... [qq] fix #548, close #443
    assert title
    title = unescape_html(title)
    title = escape_file_path(title)

    try:
        id = vid
    except:
        id = r1(r'vid:"([^"]+)"', html)

    qq_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
=======

def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
    api = "http://vv.video.qq.com/geturl?otype=json&vid=%s" % vid
    content = get_html(api)
    output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
    url = output_json['vd']['vi'][0]['url']
    _, ext, size = url_info(url, faker=True)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    content = get_html(url)
    vid = match1(content, r'vid\s*:\s*"\s*([^"]+)"')
    title = match1(content, r'title\s*:\s*"\s*([^"]+)"')

    qq_download_by_vid(vid, title, output_dir, merge, info_only)
>>>>>>> 1a58b53... [qq] reimplement qq.py, close #657

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
