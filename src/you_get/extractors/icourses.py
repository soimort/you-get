#!/usr/bin/env python
from ..common import *
from urllib import parse, error
import random
from time import sleep
import datetime
import hashlib
import base64
import logging
import re
from xml.dom.minidom import parseString

__all__ = ['icourses_download', 'icourses_playlist_download']


def icourses_download(url, output_dir='.', **kwargs):
    if 'showResDetail.action' in url:
        hit = re.search(r'id=(\d+)&courseId=(\d+)', url)
        url = 'http://www.icourses.cn/jpk/changeforVideo.action?resId={}&courseId={}'.format(hit.group(1), hit.group(2))
    if re.match(r'http://www.icourses.cn/coursestatic/course_(\d+).html', url):
        raise Exception('You can download it with -l flag')
    icourses_parser = ICousesExactor(url=url)
    icourses_parser.basic_extract()
    title = icourses_parser.title
    size = None
    for i in range(5):
        try:
            # use this url only for size
            size_url = icourses_parser.generate_url(0)
            _, type_, size = url_info(size_url, headers=fake_headers)
        except error.HTTPError:
            logging.warning('Failed to fetch the video file! Retrying...')
            sleep(random.Random().randint(2, 5))  # Prevent from blockage
        else:
            print_info(site_info, title, type_, size)
            break

    if size is None:
        raise Exception("Failed")

    if not kwargs['info_only']:
        real_url = icourses_parser.update_url(0)
        headers = fake_headers.copy()
        headers['Referer'] = url
        download_urls_icourses(real_url, title, 'flv',total_size=size, output_dir=output_dir, max_size=15728640, dyn_callback=icourses_parser.update_url)
    return


def get_course_title(url, course_type, page=None):
    if page is None:
        try:
            # shard course page could be gbk but with charset="utf-8"
            page = get_content(url, decoded=False).decode('gbk')
        except UnicodeDecodeError:
            page = get_content(url, decoded=False).decode('utf8')

    if course_type == 'shared_old':
        patt = r'<div\s+class="top_left_til">(.+?)<\/div>'
    elif course_type == 'shared_new':
        patt = r'<h1>(.+?)<\/h1>'
    else:
        patt = r'<div\s+class="con">(.+?)<\/div>'

    return re.search(patt, page).group(1)


def public_course_playlist(url, page=None):
    host = 'http://www.icourses.cn/'
    patt = r'<a href="(.+?)"\s*title="(.+?)".+?>(?:.|\n)+?</a>'

    if page is None:
        page = get_content(url)
    playlist = re.findall(patt, page)
    return [(host+i[0], i[1]) for i in playlist]


def public_course_get_title(url, page=None):
    patt = r'<div\s*class="kcslbut">.+?第(\d+)讲'

    if page is None:
        page = get_content(url)
    seq_num = int(re.search(patt, page).group(1)) - 1
    course_main_title = get_course_title(url, 'public', page)
    return '{}_第{}讲_{}'.format(course_main_title, seq_num+1, public_course_playlist(url, page)[seq_num][1])


def icourses_playlist_download(url, output_dir='.', **kwargs):
    page_type_patt = r'showSectionNode\(this,(\d+),(\d+)\)'
    resid_courseid_patt = r'changeforvideo\(\'(\d+)\',\'(\d+)\',\'(\d+)\'\)'
    ep = 'http://www.icourses.cn/jpk/viewCharacterDetail.action?sectionId={}&courseId={}'
    change_for_video_ip = 'http://www.icourses.cn/jpk/changeforVideo.action?resId={}&courseId={}'
    video_list = []

    if 'viewVCourse' in url:
        playlist = public_course_playlist(url)
        for video in playlist:
            icourses_download(video[0], output_dir=output_dir, **kwargs)
        return
    elif 'coursestatic' in url:
        course_page = get_content(url)
        page_navi_vars = re.search(page_type_patt, course_page)

        if page_navi_vars is None:  # type 2 shared course
            video_list = icourses_playlist_new(url, course_page)
        else:  # type 1 shared course
            sec_page = get_content(ep.format(page_navi_vars.group(2), page_navi_vars.group(1)))
            video_list = re.findall(resid_courseid_patt, sec_page)
    elif 'viewCharacterDetail.action' in url or 'changeforVideo.action' in url:
        page = get_content(url)
        video_list = re.findall(resid_courseid_patt, page)

    if not video_list:
        raise Exception('Unknown url pattern')

    for video in video_list:
        video_url = change_for_video_ip.format(video[0], video[1])
        sleep(random.Random().randint(0, 5))  # Prevent from blockage
        icourses_download(video_url, output_dir=output_dir, **kwargs)


def icourses_playlist_new(url, page=None):
    # 2 helpers using same interface in the js code
    def to_chap(course_id, chap_id, mod):
        ep = 'http://www.icourses.cn/jpk/viewCharacterDetail2.action?courseId={}&characId={}&mod={}'
        req = post_content(ep.format(course_id, chap_id, mod), post_data={})
        return req

    def to_sec(course_id, chap_id, mod):
        ep = 'http://www.icourses.cn/jpk/viewCharacterDetail2.action?courseId={}&characId={}&mod={}'
        req = post_content(ep.format(course_id, chap_id, mod), post_data={})
        return req

    def show_sec(course_id, chap_id):
        ep = 'http://www.icourses.cn/jpk/getSectionNode.action?courseId={}&characId={}&mod=2'
        req = post_content(ep.format(course_id, chap_id), post_data={})
        return req

    if page is None:
        page = get_content(url)
    chap_patt = r'<h3>.+?id="parent_row_(\d+)".+?onclick="(\w+)\((.+)\)"'
    to_chap_patt = r'this,(\d+),(\d+),(\d)'
    show_sec_patt = r'this,(\d+),(\d+)'
    res_patt = r'res_showResDetail\(\'(\d+)\',\'.+?\',\'\d+\',\'mp4\',\'(\d+)\'\)'
    l = re.findall(chap_patt, page)
    for i in l:
        if i[1] == 'ajaxtocharac':
            hit = re.search(to_chap_patt, i[2])
            page = to_chap(hit.group(1), hit.group(2), hit.group(3))
            hit_list = re.findall(res_patt, page)
            if hit_list:
                return get_playlist(hit_list[0][0], hit_list[0][1])
            for hit in hit_list:
                print(hit)
        elif i[1] == 'showSectionNode2':
            hit = re.search(show_sec_patt, i[2])
            page = show_sec(hit.group(1), hit.group(2))
            # print(page)
            patt = r'ajaxtosection\(this,(\d+),(\d+),(\d+)\)'
            hit_list = re.findall(patt, page)
            # print(hit_list)
            for hit in hit_list:
                page = to_sec(hit[0], hit[1], hit[2])
                vlist = re.findall(res_patt, page)
                if vlist:
                    return get_playlist(vlist[0][0], vlist[0][1])
    raise Exception("No video found in this playlist")


def get_playlist(res_id, course_id):
    ep = 'http://www.icourses.cn/jpk/changeforVideo.action?resId={}&courseId={}'
    req = get_content(ep.format(res_id, course_id))

    patt = r'<a.+?changeforvideo\(\'(\d+)\',\'(\d+)\',\'(\d+)\'\).+?title=\"(.+?)\"'
    return re.findall(patt, req)


class ICousesExactor(object):
    PLAYER_BASE_VER = '150606-1'
    ENCRYPT_MOD_VER = '151020'
    ENCRYPT_SALT = '3DAPmXsZ4o'  # It took really long time to find this...

    def __init__(self, url):
        self.url = url
        self.title = ''
        self.flashvars = ''
        self.api_data = {}
        self.media_url = ''
        self.common_args = {}
        self.enc_mode = True
        self.page = get_content(self.url)
        return

    def get_title(self):
        if 'viewVCourse' in self.url:
            self.title = public_course_get_title(self.url, self.page)
            return
        title_a_patt = r'<div class="con"> <a.*?>(.*?)</a>'
        title_b_patt = r'<div class="con"> <a.*?/a>((.|\n)*?)</div>'
        title_a = match1(self.page, title_a_patt).strip()
        title_b = match1(self.page, title_b_patt).strip()
        title = title_a + title_b
        title = re.sub('( +|\n|\t|\r|&nbsp;)', '', unescape_html(title).replace(' ', ''))
        self.title = title

    def get_flashvars(self):
        patt = r'var flashvars\s*=\s*(\{(?:.|\n)+?\});'
        hit = re.search(patt, self.page)
        if hit is None:
            raise Exception('Cannot find flashvars')
        flashvar_str = hit.group(1)

        uuid = re.search(r'uuid\s*:\s*\"?(\w+)\"?', flashvar_str).group(1)
        other = re.search(r'other\s*:\s*"(.*?)"', flashvar_str).group(1)
        isvc = re.search(r'IService\s*:\s*\'(.+?)\'', flashvar_str).group(1)

        player_time_patt = r'MPlayer.swf\?v\=(\d+)'
        player_time = re.search(player_time_patt, self.page).group(1)

        self.flashvars = dict(IService=isvc, uuid=uuid, other=other, v=player_time)

    def api_req(self, url):
        xml_str = get_content(url)
        dom = parseString(xml_str)
        status = dom.getElementsByTagName('result')[0].getAttribute('status')
        if status != 'success':
            raise Exception('API returned fail')

        api_res = {}
        meta = dom.getElementsByTagName('metadata')
        for m in meta:
            key = m.getAttribute('name')
            val = m.firstChild.nodeValue
            api_res[key] = val
        self.api_data = api_res

    def basic_extract(self):
        self.get_title()
        self.get_flashvars()
        api_req_url = '{}?{}'.format(self.flashvars['IService'], parse.urlencode(self.flashvars))
        self.api_req(api_req_url)

    def do_extract(self, received=0):
        self.basic_extract()
        return self.generate_url(received)

    def update_url(self, received):
        args = self.common_args.copy()
        play_type = 'seek' if received else 'play'
        received = received if received else -1
        args['ls'] = play_type
        args['start'] = received + 1
        args['lt'] = self.get_date_str()
        if self.enc_mode:
            ssl_ts, sign = self.get_sign(self.media_url)
            extra_args = dict(h=sign, r=ssl_ts, p=self.__class__.ENCRYPT_MOD_VER)
            args.update(extra_args)
        return '{}?{}'.format(self.media_url, parse.urlencode(args))

    @classmethod
    def get_date_str(self):
        fmt_str = '%-m-%-d/%-H:%-M:%-S'
        now = datetime.datetime.now()
        try:
            date_str =  now.strftime(fmt_str)
        except ValueError:  # msvcrt
            date_str = '{}-{}/{}:{}:{}'.format(now.month, now.day, now.hour, now.minute, now.second)
        return date_str

    def generate_url(self, received):
        media_host = self.get_media_host(self.api_data['host'])
        media_url = media_host + self.api_data['url']
        self.media_url = media_url

        common_args = dict(lv=self.__class__.PLAYER_BASE_VER)
        h = self.api_data.get('h')
        r = self.api_data.get('p', self.__class__.ENCRYPT_MOD_VER)

        if self.api_data['ssl'] != 'true':
            self.enc_mode = False
            common_args.update(dict(h=h, r=r))
        else:
            self.enc_mode = True
            common_args['p'] = self.__class__.ENCRYPT_MOD_VER
        self.common_args = common_args
        return self.update_url(received)

    def get_sign(self, media_url):
        media_host = parse.urlparse(media_url).netloc
        ran = random.randint(0, 9999999)
        ssl_callback = get_content('http://{}/ssl/ssl.shtml?r={}'.format(media_host, ran)).split(',')
        ssl_ts = int(datetime.datetime.strptime(ssl_callback[1], "%b %d %H:%M:%S %Y").timestamp() + int(ssl_callback[0]))
        sign_this = self.__class__.ENCRYPT_SALT + parse.urlparse(media_url).path + str(ssl_ts)
        arg_h = base64.b64encode(hashlib.md5(bytes(sign_this, 'utf-8')).digest(), altchars=b'-_')
        return ssl_ts, arg_h.decode('utf-8').strip('=')

    def get_media_host(self, ori_host):
        res = get_content(ori_host + '/ssl/host.shtml').strip()
        path = parse.urlparse(ori_host).path
        return ''.join([res, path])


def download_urls_icourses(url, title, ext, total_size, output_dir='.', headers=None, **kwargs):
    if dry_run or player:
        log.wtf('Non standard protocol')

    title = get_filename(title)

    filename = '%s.%s' % (title, ext)
    filepath = os.path.join(output_dir, filename)
    if not force and os.path.exists(filepath):
        print('Skipping {}: file already exists\n'.format(filepath))
        return
    bar = SimpleProgressBar(total_size, 1)
    print('Downloading %s ...' % tr(filename))
    url_save_icourses(url, filepath, bar, total_size, headers=headers, **kwargs)
    bar.done()

    print()


def url_save_icourses(url, filepath, bar, total_size, dyn_callback=None, is_part=False, max_size=0, headers=None):
    def dyn_update_url(received):
        if callable(dyn_callback):
            logging.debug('Calling callback %s for new URL from %s' % (dyn_callback.__name__, received))
            return dyn_callback(received)
    if bar is None:
        bar = DummyProgressBar()
    if os.path.exists(filepath):
        if not force:
            if not is_part:
                bar.done()
                print('Skipping %s: file already exists' % tr(os.path.basename(filepath)))
            else:
                filesize = os.path.getsize(filepath)
                bar.update_received(filesize)
            return
        else:
            if not is_part:
                bar.done()
                print('Overwriting %s' % os.path.basename(filepath), '...')
    elif not os.path.exists(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))

    temp_filepath = filepath + '.download'
    received = 0
    if not force:
        open_mode = 'ab'

        if os.path.exists(temp_filepath):
            tempfile_size = os.path.getsize(temp_filepath)
            received += tempfile_size
            bar.update_received(tempfile_size)
    else:
        open_mode = 'wb'

    if received:
        url = dyn_update_url(received)

    if headers is None:
        headers = {}
    response = urlopen_with_retry(request.Request(url, headers=headers))
# Do not update content-length here.
# Only the 1st segment's content-length is the content-length of the file.
# For other segments, content-length is the standard one, 15 * 1024 * 1024

    with open(temp_filepath, open_mode) as output:
        before_this_uri = received
# received - before_this_uri is size of the buf we get from one uri
        while True:
            update_bs = 256 * 1024
            left_bytes = total_size - received
            to_read = left_bytes if left_bytes <= update_bs else update_bs
# calc the block size to read -- The server can fail to send an EOF
            buffer = response.read(to_read)
            if not buffer:
                logging.debug('Got EOF from server')
                break
            output.write(buffer)
            received += len(buffer)
            bar.update_received(len(buffer))
            if received >= total_size:
                break
            if max_size and (received - before_this_uri) >= max_size:
                url = dyn_update_url(received)
                before_this_uri = received
                response = urlopen_with_retry(request.Request(url, headers=headers))

    assert received == os.path.getsize(temp_filepath), '%s == %s' % (received, os.path.getsize(temp_filepath))

    if os.access(filepath, os.W_OK):
        os.remove(filepath)  # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)

site_info = 'icourses.cn'
download = icourses_download
download_playlist = icourses_playlist_download
