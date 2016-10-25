#!/usr/bin/env python
from ..common import *
from urllib import parse
import random
from time import sleep
import xml.etree.ElementTree as ET
import datetime
import hashlib
import base64
import logging
from urllib import error
import re

__all__ = ['icourses_download']


def icourses_download(url, merge=False, output_dir='.', **kwargs):
    icourses_parser = ICousesExactor(url=url)
    real_url = icourses_parser.icourses_cn_url_parser(**kwargs)
    title = icourses_parser.title
    if real_url is not None:
        for tries in range(0, 5):
            try:
                _, type_, size = url_info(real_url, faker=True)
                break
            except error.HTTPError:
                logging.warning('Failed to fetch the video file! Retrying...')
                sleep(random.Random().randint(0, 5))  # Prevent from blockage
                real_url = icourses_parser.icourses_cn_url_parser()
                title = icourses_parser.title
        print_info(site_info, title, type_, size)
        if not kwargs['info_only']:
            download_urls_chunked([real_url], title, 'flv',
                          total_size=size, output_dir=output_dir, refer=url, merge=merge, faker=True, ignore_range=True, chunk_size=15000000, dyn_callback=icourses_parser.icourses_cn_url_parser)


# Why not using VideoExtractor: This site needs specical download method
class ICousesExactor(object):

    def __init__(self, url):
        self.url = url
        self.title = ''
        return

    def icourses_playlist_download(self, **kwargs):
        html = get_content(self.url)
        page_type_patt = r'showSectionNode\(this,(\d+),(\d+)\)'
        video_js_number = r'changeforvideo\((.*?)\)'
        fs_flag = r'<input type="hidden" value=(\w+) id="firstShowFlag">'
        page_navi_vars = re.search(pattern=page_type_patt, string=html)
        dummy_page = 'http://www.icourses.cn/jpk/viewCharacterDetail.action?sectionId={}&courseId={}'.format(
            page_navi_vars.group(2), page_navi_vars.group(1))
        html = get_content(dummy_page)
        fs_status = match1(html, fs_flag)
        video_list = re.findall(pattern=video_js_number, string=html)
        for video in video_list:
            video_args = video.replace('\'', '').split(',')
            video_url = 'http://www.icourses.cn/jpk/changeforVideo.action?resId={}&courseId={}&firstShowFlag={}'.format(
                video_args[0], video_args[1], fs_status or '1')
            sleep(random.Random().randint(0, 5))  # Prevent from blockage
            icourses_download(video_url, **kwargs)

    def icourses_cn_url_parser(self, received=0, **kwargs):
        PLAYER_BASE_VER = '150606-1'
        ENCRYPT_MOD_VER = '151020'
        ENCRYPT_SALT = '3DAPmXsZ4o'  # It took really long time to find this...
        html = get_content(self.url)
        if re.search(pattern=r'showSectionNode\(.*\)', string=html):
            logging.warning('Switching to playlist mode!')
            return self.icourses_playlist_download(**kwargs)
        flashvars_patt = r'var\ flashvars\=((.|\n)*)};'
        server_time_patt = r'MPlayer.swf\?v\=(\d+)'
        uuid_patt = r'uuid:(\d+)'
        other_args_patt = r'other:"(.*)"'
        res_url_patt = r'IService:\'([^\']+)'
        title_a_patt = r'<div class="con"> <a.*?>(.*?)</a>'
        title_b_patt = r'<div class="con"> <a.*?/a>((.|\n)*?)</div>'
        title_a = match1(html, title_a_patt).strip()
        title_b = match1(html, title_b_patt).strip()
        title = title_a + title_b  # WIP, FIXME
        title = re.sub('( +|\n|\t|\r|\&nbsp\;)', '',
                       unescape_html(title).replace(' ', ''))
        server_time = match1(html, server_time_patt)
        flashvars = match1(html, flashvars_patt)
        uuid = match1(flashvars, uuid_patt)
        other_args = match1(flashvars, other_args_patt)
        res_url = match1(flashvars, res_url_patt)
        url_parts = {'v': server_time, 'other': other_args,
                     'uuid': uuid, 'IService': res_url}
        req_url = '%s?%s' % (res_url, parse.urlencode(url_parts))
        logging.debug('Requesting video resource location...')
        xml_resp = get_html(req_url)
        xml_obj = ET.fromstring(xml_resp)
        logging.debug('The result was {}'.format(xml_obj.get('status')))
        if xml_obj.get('status') != 'success':
            raise ValueError('Server returned error!')
        if received:
            play_type = 'seek'
        else:
            play_type = 'play'
            received -= 1
        common_args = {'lv': PLAYER_BASE_VER, 'ls': play_type,
                       'lt': datetime.datetime.now().strftime('%m-%d/%H:%M:%S'),
                       'start': received + 1}
        media_host = xml_obj.find(".//*[@name='host']").text
        media_url = media_host + xml_obj.find(".//*[@name='url']").text
        # This is what they called `SSLModule`... But obviously, just a kind of
        # encryption, takes absolutely no effect in protecting data intergrity
        if xml_obj.find(".//*[@name='ssl']").text != 'true':
            logging.debug('The encryption mode is disabled')
            # when the so-called `SSLMode` is not activated, the parameters, `h`
            # and `p` can be found in response
            arg_h = xml_obj.find(".//*[@name='h']").text
            assert arg_h
            arg_r = xml_obj.find(".//*[@name='p']").text or ENCRYPT_MOD_VER
            url_args = common_args.copy()
            url_args.update({'h': arg_h, 'r': arg_r})
            final_url = '{}?{}'.format(
                media_url, parse.urlencode(url_args))
            self.title = title
            return final_url
        # when the `SSLMode` is activated, we need to receive the timestamp and the
        # time offset (?) value from the server
        logging.debug('The encryption mode is in effect')
        ssl_callback = get_html(
            '{}/ssl/ssl.shtml'.format(media_host)).split(',')
        ssl_timestamp = int(datetime.datetime.strptime(
            ssl_callback[1], "%b %d %H:%M:%S %Y").timestamp() + int(ssl_callback[0]))
        sign_this = ENCRYPT_SALT + \
            parse.urlparse(media_url).path + str(ssl_timestamp)
        arg_h = base64.b64encode(hashlib.md5(
            bytes(sign_this, 'utf-8')).digest())
        # Post-processing, may subject to change, so leaving this alone...
        arg_h = arg_h.decode('utf-8').strip('=').replace('+',
                                                         '-').replace('/', '_')
        arg_r = ssl_timestamp
        url_args = common_args.copy()
        url_args.update({'h': arg_h, 'r': arg_r, 'p': ENCRYPT_MOD_VER})
        final_url = '{}?{}'.format(
            media_url, parse.urlencode(url_args))
        logging.debug('Crafted URL: {}'.format(final_url))
        self.title = title
        return final_url


site_info = 'icourses.cn'
download = icourses_download
# download_playlist = icourses_playlist_download
