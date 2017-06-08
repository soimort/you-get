#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *
from .qie import download as qieDownload
from urllib.parse import urlparse,parse_qs

def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
    info_api = 'http://vv.video.qq.com/getinfo?otype=json&appver=3%2E2%2E19%2E333&platform=11&defnpayver=1&vid=' + vid
    info = get_html(info_api)
    video_json = json.loads(match1(info, r'QZOutputJson=(.*)')[:-1])
    parts_vid = video_json['vl']['vi'][0]['vid']
    parts_ti = video_json['vl']['vi'][0]['ti']
    parts_prefix = video_json['vl']['vi'][0]['ul']['ui'][0]['url']
    parts_formats = video_json['fl']['fi']
    if parts_prefix.endswith('/'):
        parts_prefix = parts_prefix[:-1]
    # find best quality
    # only looking for fhd(1080p) and shd(720p) here.
    # 480p usually come with a single file, will be downloaded as fallback.
    best_quality = ''
    for part_format in parts_formats:
        if part_format['name'] == 'fhd':
            best_quality = 'fhd'
            break

        if part_format['name'] == 'shd':
            best_quality = 'shd'

    for part_format in parts_formats:
        if (not best_quality == '') and (not part_format['name'] == best_quality):
            continue
        part_format_id = part_format['id']
        part_format_sl = part_format['sl']
        if part_format_sl == 0:
            part_urls= []
            total_size = 0
            try:
                # For fhd(1080p), every part is about 100M and 6 minutes
                # try 100 parts here limited download longest single video of 10 hours.
                for part in range(1,100):
                    filename = vid + '.p' + str(part_format_id % 10000) + '.' + str(part) + '.mp4'
                    key_api = "http://vv.video.qq.com/getkey?otype=json&platform=11&format=%s&vid=%s&filename=%s" % (part_format_id, parts_vid, filename)
                    #print(filename)
                    #print(key_api)
                    part_info = get_html(key_api)
                    key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
                    #print(key_json)
                    vkey = key_json['key']
                    url = '%s/%s?vkey=%s' % (parts_prefix, filename, vkey)
                    part_urls.append(url)
                    _, ext, size = url_info(url, faker=True)
                    total_size += size
            except:
                pass
            print_info(site_info, parts_ti, ext, total_size)
            if not info_only:
                download_urls(part_urls, parts_ti, ext, total_size, output_dir=output_dir, merge=merge)
        else:
            fvkey = video_json['vl']['vi'][0]['fvkey']
            mp4 = video_json['vl']['vi'][0]['cl'].get('ci', None)
            if mp4:
                old_id = mp4[0]['keyid'].split('.')[1]
                new_id = 'p' + str(int(old_id) % 10000)
                mp4 = mp4[0]['keyid'].replace(old_id, new_id) + '.mp4'
            else:
                mp4 = video_json['vl']['vi'][0]['fn']
            url = '%s/%s?vkey=%s' % ( parts_prefix, mp4, fvkey )
            _, ext, size = url_info(url, faker=True)

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def kg_qq_download_by_shareid(shareid, output_dir='.', info_only=False, caption=False):
    BASE_URL = 'http://cgi.kg.qq.com/fcgi-bin/kg_ugc_getdetail'
    params_str = '?dataType=jsonp&jsonp=callback&jsonpCallback=jsopgetsonginfo&v=4&outCharset=utf-8&shareid=' + shareid
    url = BASE_URL + params_str
    content = get_content(url)
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
    if 'kg.qq.com' in url or 'kg2.qq.com' in url:
        shareid = url.split('?s=')[-1]
        caption = kwargs['caption']
        kg_qq_download_by_shareid(shareid, output_dir=output_dir, info_only=info_only, caption=caption)
        return

    if 'live.qq.com' in url:
        qieDownload(url, output_dir=output_dir, merge=merge, info_only=info_only)
        return

    if 'mp.weixin.qq.com/s?' in url:
        content = get_html(url)
        vids = matchall(content, [r'\bvid=(\w+)'])
        for vid in vids:
            qq_download_by_vid(vid, vid, output_dir, merge, info_only)
        return

    #do redirect
    if 'v.qq.com/page' in url:
        # for URLs like this:
        # http://v.qq.com/page/k/9/7/k0194pwgw97.html
        new_url = url_locations([url])[0]
        if url == new_url:
            #redirect in js?
            content = get_content(url)
            url = match1(content,r'window\.location\.href="(.*?)"')
        else:
            url = new_url

    if 'kuaibao.qq.com' in url or re.match(r'http://daxue.qq.com/content/content/id/\d+', url):
        content = get_html(url)
        vid = match1(content, r'vid\s*=\s*"\s*([^"]+)"')
        title = match1(content, r'title">([^"]+)</p>')
        title = title.strip() if title else vid
    elif 'iframe/player.html' in url:
        vid = match1(url, r'\bvid=(\w+)')
        # for embedded URLs; don't know what the title is
        title = vid
    else:
        content = get_html(url)
        vid = parse_qs(urlparse(url).query).get('vid') #for links specified vid  like http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5
        vid = vid[0] if vid else match1(content, r'vid"*\s*:\s*"\s*([^"]+)"') #general fallback
        title = match1(content,r'<a.*?id\s*=\s*"%s".*?title\s*=\s*"(.+?)".*?>'%vid)
        title = match1(content, r'title">([^"]+)</p>') if not title else title
        title = match1(content, r'"title":"([^"]+)"') if not title else title
        title = vid if not title else title #general fallback

    qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
