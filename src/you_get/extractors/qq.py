#!/usr/bin/env python

__all__ = ['qq_download']

from .qie import download as qieDownload
from .qie_video import download_by_url as qie_video_download
from ..common import *

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  QQLive/10275340/50192209 Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.561.202 QQBrowser/9.0.2524.400'
}


def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):

    # http://v.sports.qq.com/#/cover/t0fqsm1y83r8v5j/a0026nvw5jr https://v.qq.com/x/cover/t0fqsm1y83r8v5j/a0026nvw5jr.html
    video_json = None
    platforms = [4100201, 11]
    for platform in platforms:
        info_api = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform={}&defnpayver=1&defn=shd&vid={}'.format(platform, vid)
        info = get_content(info_api, headers)
        video_json = json.loads(match1(info, r'QZOutputJson=(.*)')[:-1])
        if not video_json.get('msg')=='cannot play outside':
            break
    fn_pre = video_json['vl']['vi'][0]['lnk']
    title = video_json['vl']['vi'][0]['ti']
    host = video_json['vl']['vi'][0]['ul']['ui'][0]['url']
    seg_cnt = fc_cnt = video_json['vl']['vi'][0]['cl']['fc']

    filename = video_json['vl']['vi'][0]['fn']
    if seg_cnt == 0:
        seg_cnt = 1
    else:
        fn_pre, magic_str, video_type = filename.split('.')

    part_urls= []
    total_size = 0
    for part in range(1, seg_cnt+1):
        if fc_cnt == 0:
            # fix json parsing error
            # example:https://v.qq.com/x/page/w0674l9yrrh.html
            part_format_id = video_json['vl']['vi'][0]['cl']['keyid'].split('.')[-1]
        else:
            part_format_id = video_json['vl']['vi'][0]['cl']['ci'][part - 1]['keyid'].split('.')[1]
            filename = '.'.join([fn_pre, magic_str, str(part), video_type])

        key_api = "http://vv.video.qq.com/getkey?otype=json&platform=11&format={}&vid={}&filename={}&appver=3.2.19.333".format(part_format_id, vid, filename)
        part_info = get_content(key_api, headers)
        key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
        if key_json.get('key') is None:
            vkey = video_json['vl']['vi'][0]['fvkey']
            url = '{}{}?vkey={}'.format(video_json['vl']['vi'][0]['ul']['ui'][0]['url'], fn_pre + '.mp4', vkey)
        else:
            vkey = key_json['key']
            url = '{}{}?vkey={}'.format(host, filename, vkey)
        if not vkey:
            if part == 1:
                log.wtf(key_json['msg'])
            else:
                log.w(key_json['msg'])
            break
        if key_json.get('filename') is None:
            log.w(key_json['msg'])
            break

        part_urls.append(url)
        _, ext, size = url_info(url)
        total_size += size

    print_info(site_info, title, ext, total_size)
    if not info_only:
        download_urls(part_urls, title, ext, total_size, output_dir=output_dir, merge=merge)

def kg_qq_download_by_shareid(shareid, output_dir='.', info_only=False, caption=False):
    BASE_URL = 'http://cgi.kg.qq.com/fcgi-bin/kg_ugc_getdetail'
    params_str = '?dataType=jsonp&jsonp=callback&jsonpCallback=jsopgetsonginfo&v=4&outCharset=utf-8&shareid=' + shareid
    url = BASE_URL + params_str
    content = get_content(url, headers)
    json_str = content[len('jsonpcallback('):-1]
    json_data = json.loads(json_str)

    playurl = json_data['data']['playurl']
    videourl = json_data['data']['playurl_video']
    real_url = playurl if playurl else videourl
    real_url = real_url.replace('\/', '/')

    ksong_mid = json_data['data']['ksong_mid']
    lyric_url = 'http://cgi.kg.qq.com/fcgi-bin/fcg_lyric?jsonpCallback=jsopgetlrcdata&outCharset=utf-8&ksongmid=' + ksong_mid
    lyric_data = get_content(lyric_url)
    lyric_string = lyric_data[len('jsopgetlrcdata('):-1]
    lyric_json = json.loads(lyric_string)
    lyric = lyric_json['data']['lyric']

    title = match1(lyric, r'\[ti:([^\]]*)\]')

    type, ext, size = url_info(real_url)
    if not title:
        title = shareid

    print_info('腾讯全民K歌', title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge=False)
        if caption:
            caption_filename = title + '.lrc'
            caption_path = output_dir + '/' + caption_filename
            with open(caption_path, 'w') as f:
                lrc_list = lyric.split('\r\n')
                for line in lrc_list:
                    f.write(line)
                    f.write('\n')

def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """"""

    if re.match(r'https?://(m\.)?egame.qq.com/', url):
        from . import qq_egame
        qq_egame.qq_egame_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    if 'kg.qq.com' in url or 'kg2.qq.com' in url:
        shareid = url.split('?s=')[-1]
        caption = kwargs['caption']
        kg_qq_download_by_shareid(shareid, output_dir=output_dir, info_only=info_only, caption=caption)
        return

    if 'live.qq.com' in url:
        if 'live.qq.com/video/v' in url:
            qie_video_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        else:
            qieDownload(url, output_dir=output_dir, merge=merge, info_only=info_only)
        return

    if 'mp.weixin.qq.com/s' in url:
        content = get_content(url, headers)
        vids = matchall(content, [r'[?;]vid=(\w+)'])
        for vid in vids:
            qq_download_by_vid(vid, vid, output_dir, merge, info_only)
        return

    if 'kuaibao.qq.com/s/' in url:
        # https://kuaibao.qq.com/s/20180521V0Z9MH00
        nid = match1(url, r'/s/([^/&?#]+)')
        content = get_content('https://kuaibao.qq.com/getVideoRelate?id=' + nid)
        info_json = json.loads(content)
        vid=info_json['videoinfo']['vid']
        title=info_json['videoinfo']['title']
    elif 'kuaibao.qq.com' in url or re.match(r'http://daxue.qq.com/content/content/id/\d+', url):
        # http://daxue.qq.com/content/content/id/2321
        content = get_content(url, headers)
        vid = match1(content, r'vid\s*=\s*"\s*([^"]+)"')
        title = match1(content, r'title">([^"]+)</p>')
        title = title.strip() if title else vid
    elif 'iframe/player.html' in url:
        vid = match1(url, r'\bvid=(\w+)')
        # for embedded URLs; don't know what the title is
        title = vid
    elif 'view.inews.qq.com' in url:
        # view.inews.qq.com/a/20180521V0Z9MH00
        content = get_content(url, headers)
        vid = match1(content, r'"vid":"(\w+)"')
        title = match1(content, r'"title":"(\w+)"')
    else:
        content = get_content(url, headers)
        #vid = parse_qs(urlparse(url).query).get('vid') #for links specified vid  like http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5
        rurl = match1(content, r'<link.*?rel\s*=\s*"canonical".*?href\s*="(.+?)".*?>') #https://v.qq.com/x/cover/9hpjiv5fhiyn86u/t0522x58xma.html
        vid = ""
        if rurl:
            vid = rurl.split('/')[-1].split('.')[0]
            # https://v.qq.com/x/page/d0552xbadkl.html https://y.qq.com/n/yqq/mv/v/g00268vlkzy.html
            if vid == "undefined" or vid == "index":
                vid = ""
        vid = vid if vid else url.split('/')[-1].split('.')[0] #https://v.qq.com/x/cover/ps6mnfqyrfo7es3/q0181hpdvo5.html?
        vid = vid if vid else match1(content, r'vid"*\s*:\s*"\s*([^"]+)"') #general fallback
        if not vid:
            vid = match1(content, r'id"*\s*:\s*"(.+?)"')
        title = match1(content,r'<a.*?id\s*=\s*"%s".*?title\s*=\s*"(.+?)".*?>'%vid)
        title = match1(content, r'title">([^"]+)</p>') if not title else title
        title = match1(content, r'"title":"([^"]+)"') if not title else title
        title = vid if not title else title #general fallback


    qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
