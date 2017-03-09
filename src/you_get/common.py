#!/usr/bin/env python

SITES = {
    '163'              : 'netease',
    '56'               : 'w56',
    'acfun'            : 'acfun',
    'archive'          : 'archive',
    'baidu'            : 'baidu',
    'bandcamp'         : 'bandcamp',
    'baomihua'         : 'baomihua',
    'bigthink'         : 'bigthink',
    'bilibili'         : 'bilibili',
    'cctv'             : 'cntv',
    'cntv'             : 'cntv',
    'cbs'              : 'cbs',
    'dailymotion'      : 'dailymotion',
    'dilidili'         : 'dilidili',
    'douban'           : 'douban',
    'douyu'            : 'douyutv',
    'ehow'             : 'ehow',
    'facebook'         : 'facebook',
    'fc2'              : 'fc2video',
    'flickr'           : 'flickr',
    'freesound'        : 'freesound',
    'fun'              : 'funshion',
    'google'           : 'google',
    'heavy-music'      : 'heavymusic',
    'huaban'           : 'huaban',
    'huomao'           : 'huomaotv',
    'iask'             : 'sina',
    'icourses'         : 'icourses',
    'ifeng'            : 'ifeng',
    'imgur'            : 'imgur',
    'in'               : 'alive',
    'infoq'            : 'infoq',
    'instagram'        : 'instagram',
    'interest'         : 'interest',
    'iqilu'            : 'iqilu',
    'iqiyi'            : 'iqiyi',
    'isuntv'           : 'suntv',
    'joy'              : 'joy',
    'kankanews'        : 'bilibili',
    'khanacademy'      : 'khan',
    'ku6'              : 'ku6',
    'kugou'            : 'kugou',
    'kuwo'             : 'kuwo',
    'le'               : 'le',
    'letv'             : 'le',
    'lizhi'            : 'lizhi',
    'magisto'          : 'magisto',
    'metacafe'         : 'metacafe',
    'mgtv'             : 'mgtv',
    'miomio'           : 'miomio',
    'mixcloud'         : 'mixcloud',
    'mtv81'            : 'mtv81',
    'musicplayon'      : 'musicplayon',
    'naver'            : 'naver',
    '7gogo'            : 'nanagogo',
    'nicovideo'        : 'nicovideo',
    'panda'            : 'panda',
    'pinterest'        : 'pinterest',
    'pixnet'           : 'pixnet',
    'pptv'             : 'pptv',
    'qq'               : 'qq',
    'quanmin'          : 'quanmin',
    'showroom-live'    : 'showroom',
    'sina'             : 'sina',
    'smgbb'            : 'bilibili',
    'sohu'             : 'sohu',
    'soundcloud'       : 'soundcloud',
    'ted'              : 'ted',
    'theplatform'      : 'theplatform',
    'tucao'            : 'tucao',
    'tudou'            : 'tudou',
    'tumblr'           : 'tumblr',
    'twimg'            : 'twitter',
    'twitter'          : 'twitter',
    'videomega'        : 'videomega',
    'vidto'            : 'vidto',
    'vimeo'            : 'vimeo',
    'wanmen'           : 'wanmen',
    'weibo'            : 'miaopai',
    'veoh'             : 'veoh',
    'vine'             : 'vine',
    'vk'               : 'vk',
    'xiami'            : 'xiami',
    'xiaokaxiu'        : 'yixia',
    'xiaojiadianvideo' : 'fc2video',
    'yinyuetai'        : 'yinyuetai',
    'miaopai'          : 'yixia',
    'youku'            : 'youku',
    'youtu'            : 'youtube',
    'youtube'          : 'youtube',
    'zhanqi'           : 'zhanqi',
}

import getopt
import json
import locale
import logging
import os
import platform
import re
import socket
import sys
import time
from urllib import request, parse, error
from http import cookiejar
from importlib import import_module

from .version import __version__
from .util import log, term
from .util.git import get_version
from .util.strings import get_filename, unescape_html
from . import json_output as json_output_

dry_run = False
json_output = False
force = False
player = None
extractor_proxy = None
cookies = None
output_filename = None

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
}

if sys.stdout.isatty():
    default_encoding = sys.stdout.encoding.lower()
else:
    default_encoding = locale.getpreferredencoding().lower()

def maybe_print(*s):
    try: print(*s)
    except: pass

def tr(s):
    if default_encoding == 'utf-8':
        return s
    else:
        return s
        #return str(s.encode('utf-8'))[2:-1]

# DEPRECATED in favor of match1()
def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

# DEPRECATED in favor of match1()
def r1_of(patterns, text):
    for p in patterns:
        x = r1(p, text)
        if x:
            return x

def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).

    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.

    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret

def matchall(text, patterns):
    """Scans through a string for substrings matched some patterns.

    Args:
        text: A string to be scanned.
        patterns: a list of regex pattern.

    Returns:
        a list if matched. empty if not.
    """

    ret = []
    for pattern in patterns:
        match = re.findall(pattern, text)
        ret += match

    return ret

def launch_player(player, urls):
    import subprocess
    import shlex
    subprocess.call(shlex.split(player) + list(urls))

def parse_query_param(url, param):
    """Parses the query string of a URL and returns the value of a parameter.

    Args:
        url: A URL.
        param: A string representing the name of the parameter.

    Returns:
        The value of the parameter.
    """

    try:
        return parse.parse_qs(parse.urlparse(url).query)[param][0]
    except:
        return None

def unicodize(text):
    return re.sub(r'\\u([0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])', lambda x: chr(int(x.group(0)[2:], 16)), text)

# DEPRECATED in favor of util.legitimize()
def escape_file_path(path):
    path = path.replace('/', '-')
    path = path.replace('\\', '-')
    path = path.replace('*', '-')
    path = path.replace('?', '-')
    return path

def ungzip(data):
    """Decompresses data for Content-Encoding: gzip.
    """
    from io import BytesIO
    import gzip
    buffer = BytesIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()

def undeflate(data):
    """Decompresses data for Content-Encoding: deflate.
    (the zlib compression is used.)
    """
    import zlib
    decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
    return decompressobj.decompress(data)+decompressobj.flush()

# DEPRECATED in favor of get_content()
def get_response(url, faker = False):
    # install cookies
    if cookies:
        opener = request.build_opener(request.HTTPCookieProcessor(cookies))
        request.install_opener(opener)

    if faker:
        response = request.urlopen(request.Request(url, headers = fake_headers), None)
    else:
        response = request.urlopen(url)

    data = response.read()
    if response.info().get('Content-Encoding') == 'gzip':
        data = ungzip(data)
    elif response.info().get('Content-Encoding') == 'deflate':
        data = undeflate(data)
    response.data = data
    return response

# DEPRECATED in favor of get_content()
def get_html(url, encoding = None, faker = False):
    content = get_response(url, faker).data
    return str(content, 'utf-8', 'ignore')

# DEPRECATED in favor of get_content()
def get_decoded_html(url, faker = False):
    response = get_response(url, faker)
    data = response.data
    charset = r1(r'charset=([\w-]+)', response.headers['content-type'])
    if charset:
        return data.decode(charset, 'ignore')
    else:
        return data

def get_location(url):
    response = request.urlopen(url)
    # urllib will follow redirections and it's too much code to tell urllib
    # not to do that
    return response.geturl()

def urlopen_with_retry(*args, **kwargs):
    for i in range(10):
        try:
            return request.urlopen(*args, **kwargs)
        except socket.timeout:
            logging.debug('request attempt %s timeout' % str(i + 1))

def get_content(url, headers={}, decoded=True):
    """Gets the content of a URL via sending a HTTP GET request.

    Args:
        url: A URL.
        headers: Request headers used by the client.
        decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

    Returns:
        The content as a string.
    """

    logging.debug('get_content: %s' % url)

    req = request.Request(url, headers=headers)
    if cookies:
        cookies.add_cookie_header(req)
        req.headers.update(req.unredirected_hdrs)

    response = urlopen_with_retry(req)
    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    if decoded:
        charset = match1(response.getheader('Content-Type'), r'charset=([\w-]+)')
        if charset is not None:
            data = data.decode(charset)
        else:
            data = data.decode('utf-8', 'ignore')

    return data

def post_content(url, headers={}, post_data={}, decoded=True):
    """Post the content of a URL via sending a HTTP POST request.

    Args:
        url: A URL.
        headers: Request headers used by the client.
        decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

    Returns:
        The content as a string.
    """

    logging.debug('post_content: %s \n post_data: %s' % (url, post_data))

    req = request.Request(url, headers=headers)
    if cookies:
        cookies.add_cookie_header(req)
        req.headers.update(req.unredirected_hdrs)
    post_data_enc = bytes(parse.urlencode(post_data), 'utf-8')
    response = urlopen_with_retry(req, data=post_data_enc)
    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    if decoded:
        charset = match1(response.getheader('Content-Type'), r'charset=([\w-]+)')
        if charset is not None:
            data = data.decode(charset)
        else:
            data = data.decode('utf-8')

    return data

def url_size(url, faker = False, headers = {}):
    if faker:
        response = urlopen_with_retry(request.Request(url, headers=fake_headers))
    elif headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(url)

    size = response.headers['content-length']
    return int(size) if size!=None else float('inf')

def urls_size(urls, faker = False, headers = {}):
    return sum([url_size(url, faker=faker, headers=headers) for url in urls])

def get_head(url, headers = {}, get_method = 'HEAD'):
    if headers:
        req = request.Request(url, headers=headers)
    else:
        req = request.Request(url)
    req.get_method = lambda: get_method
    res = urlopen_with_retry(req)
    return dict(res.headers)

def url_info(url, faker = False, headers = {}):
    if faker:
        response = urlopen_with_retry(request.Request(url, headers=fake_headers))
    elif headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(request.Request(url))

    headers = response.headers

    type = headers['content-type']
    if type == 'image/jpg; charset=UTF-8' or type == 'image/jpg' : type = 'audio/mpeg'    #fix for netease
    mapping = {
        'video/3gpp': '3gp',
        'video/f4v': 'flv',
        'video/mp4': 'mp4',
        'video/MP2T': 'ts',
        'video/quicktime': 'mov',
        'video/webm': 'webm',
        'video/x-flv': 'flv',
        'video/x-ms-asf': 'asf',
        'audio/mp4': 'mp4',
        'audio/mpeg': 'mp3',
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/gif': 'gif',
        'application/pdf': 'pdf',
    }
    if type in mapping:
        ext = mapping[type]
    else:
        type = None
        if headers['content-disposition']:
            try:
                filename = parse.unquote(r1(r'filename="?([^"]+)"?', headers['content-disposition']))
                if len(filename.split('.')) > 1:
                    ext = filename.split('.')[-1]
                else:
                    ext = None
            except:
                ext = None
        else:
            ext = None

    if headers['transfer-encoding'] != 'chunked':
        size = headers['content-length'] and int(headers['content-length'])
    else:
        size = None

    return type, ext, size

def url_locations(urls, faker = False, headers = {}):
    locations = []
    for url in urls:
        if faker:
            response = urlopen_with_retry(request.Request(url, headers=fake_headers))
        elif headers:
            response = urlopen_with_retry(request.Request(url, headers=headers))
        else:
            response = urlopen_with_retry(request.Request(url))

        locations.append(response.url)
    return locations

def url_save(url, filepath, bar, refer = None, is_part = False, faker = False, headers = {}):
    file_size = url_size(url, faker = faker, headers = headers)

    if os.path.exists(filepath):
        if not force and file_size == os.path.getsize(filepath):
            if not is_part:
                if bar:
                    bar.done()
                print('Skipping %s: file already exists' % tr(os.path.basename(filepath)))
            else:
                if bar:
                    bar.update_received(file_size)
            return
        else:
            if not is_part:
                if bar:
                    bar.done()
                print('Overwriting %s' % tr(os.path.basename(filepath)), '...')
    elif not os.path.exists(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))

    temp_filepath = filepath + '.download' if file_size!=float('inf') else filepath
    received = 0
    if not force:
        open_mode = 'ab'

        if os.path.exists(temp_filepath):
            received += os.path.getsize(temp_filepath)
            if bar:
                bar.update_received(os.path.getsize(temp_filepath))
    else:
        open_mode = 'wb'

    if received < file_size:
        if faker:
            headers = fake_headers
        elif headers:
            headers = headers
        else:
            headers = {}
        if received:
            headers['Range'] = 'bytes=' + str(received) + '-'
        if refer:
            headers['Referer'] = refer

        response = urlopen_with_retry(request.Request(url, headers=headers))
        try:
            range_start = int(response.headers['content-range'][6:].split('/')[0].split('-')[0])
            end_length = int(response.headers['content-range'][6:].split('/')[1])
            range_length = end_length - range_start
        except:
            content_length = response.headers['content-length']
            range_length = int(content_length) if content_length!=None else float('inf')

        if file_size != received + range_length:
            received = 0
            if bar:
                bar.received = 0
            open_mode = 'wb'

        with open(temp_filepath, open_mode) as output:
            while True:
                buffer = response.read(1024 * 256)
                if not buffer:
                    if received == file_size: # Download finished
                        break
                    else: # Unexpected termination. Retry request
                        headers['Range'] = 'bytes=' + str(received) + '-'
                        response = urlopen_with_retry(request.Request(url, headers=headers))
                output.write(buffer)
                received += len(buffer)
                if bar:
                    bar.update_received(len(buffer))

    assert received == os.path.getsize(temp_filepath), '%s == %s == %s' % (received, os.path.getsize(temp_filepath), temp_filepath)

    if os.access(filepath, os.W_OK):
        os.remove(filepath) # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)

def url_save_chunked(url, filepath, bar, dyn_callback=None, chunk_size=0, ignore_range=False, refer=None, is_part=False, faker=False, headers={}):
    def dyn_update_url(received):
        if callable(dyn_callback):
            logging.debug('Calling callback %s for new URL from %s' % (dyn_callback.__name__, received))
            return dyn_callback(received)
    if os.path.exists(filepath):
        if not force:
            if not is_part:
                if bar:
                    bar.done()
                print('Skipping %s: file already exists' % tr(os.path.basename(filepath)))
            else:
                if bar:
                    bar.update_received(os.path.getsize(filepath))
            return
        else:
            if not is_part:
                if bar:
                    bar.done()
                print('Overwriting %s' % tr(os.path.basename(filepath)), '...')
    elif not os.path.exists(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))

    temp_filepath = filepath + '.download'
    received = 0
    if not force:
        open_mode = 'ab'

        if os.path.exists(temp_filepath):
            received += os.path.getsize(temp_filepath)
            if bar:
                bar.update_received(os.path.getsize(temp_filepath))
    else:
        open_mode = 'wb'

    if faker:
        headers = fake_headers
    elif headers:
        headers = headers
    else:
        headers = {}
    if received:
        url = dyn_update_url(received)
        if not ignore_range:
            headers['Range'] = 'bytes=' + str(received) + '-'
    if refer:
        headers['Referer'] = refer

    response = urlopen_with_retry(request.Request(url, headers=headers))

    with open(temp_filepath, open_mode) as output:
        this_chunk = received
        while True:
            buffer = response.read(1024 * 256)
            if not buffer:
                break
            output.write(buffer)
            received += len(buffer)
            if chunk_size and (received - this_chunk) >= chunk_size:
                url = dyn_callback(received)
                this_chunk = received
                response = urlopen_with_retry(request.Request(url, headers=headers))
            if bar:
                bar.update_received(len(buffer))

    assert received == os.path.getsize(temp_filepath), '%s == %s == %s' % (received, os.path.getsize(temp_filepath))

    if os.access(filepath, os.W_OK):
        os.remove(filepath) # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)

class SimpleProgressBar:
    term_size = term.get_terminal_size()[1]

    def __init__(self, total_size, total_pieces = 1):
        self.displayed = False
        self.total_size = total_size
        self.total_pieces = total_pieces
        self.current_piece = 1
        self.received = 0
        self.speed = ''
        self.last_updated = time.time()

        total_pieces_len = len(str(total_pieces))
        # 38 is the size of all statically known size in self.bar
        total_str = '%5s' % round(self.total_size / 1048576, 1)
        total_str_width = max(len(total_str), 5)
        self.bar_size = self.term_size - 27 - 2*total_pieces_len - 2*total_str_width
        self.bar = '{:>4}%% ({:>%s}/%sMB) ├{:─<%s}┤[{:>%s}/{:>%s}] {}' % (
            total_str_width, total_str, self.bar_size, total_pieces_len, total_pieces_len)

    def update(self):
        self.displayed = True
        bar_size = self.bar_size
        percent = round(self.received * 100 / self.total_size, 1)
        if percent >= 100:
            percent = 100
        dots = bar_size * int(percent) // 100
        plus = int(percent) - dots // bar_size * 100
        if plus > 0.8:
            plus = '█'
        elif plus > 0.4:
            plus = '>'
        else:
            plus = ''
        bar = '█' * dots + plus
        bar = self.bar.format(percent, round(self.received / 1048576, 1), bar, self.current_piece, self.total_pieces, self.speed)
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

    def update_received(self, n):
        self.received += n
        time_diff = time.time() - self.last_updated
        bytes_ps = n / time_diff if time_diff else 0
        if bytes_ps >= 1024 ** 3:
            self.speed = '{:4.0f} GB/s'.format(bytes_ps / 1024 ** 3)
        elif bytes_ps >= 1024 ** 2:
            self.speed = '{:4.0f} MB/s'.format(bytes_ps / 1024 ** 2)
        elif bytes_ps >= 1024:
            self.speed = '{:4.0f} kB/s'.format(bytes_ps / 1024)
        else:
            self.speed = '{:4.0f}  B/s'.format(bytes_ps)
        self.last_updated = time.time()
        self.update()

    def update_piece(self, n):
        self.current_piece = n

    def done(self):
        if self.displayed:
            print()
            self.displayed = False

class PiecesProgressBar:
    def __init__(self, total_size, total_pieces = 1):
        self.displayed = False
        self.total_size = total_size
        self.total_pieces = total_pieces
        self.current_piece = 1
        self.received = 0

    def update(self):
        self.displayed = True
        bar = '{0:>5}%[{1:<40}] {2}/{3}'.format('', '=' * 40, self.current_piece, self.total_pieces)
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

    def update_received(self, n):
        self.received += n
        self.update()

    def update_piece(self, n):
        self.current_piece = n

    def done(self):
        if self.displayed:
            print()
            self.displayed = False

class DummyProgressBar:
    def __init__(self, *args):
        pass
    def update_received(self, n):
        pass
    def update_piece(self, n):
        pass
    def done(self):
        pass

def get_output_filename(urls, title, ext, output_dir, merge):
    # lame hack for the --output-filename option
    global output_filename
    if output_filename: return output_filename

    merged_ext = ext
    if (len(urls) > 1) and merge:
        from .processor.ffmpeg import has_ffmpeg_installed
        if ext in ['flv', 'f4v']:
            if has_ffmpeg_installed():
                merged_ext = 'mp4'
            else:
                merged_ext = 'flv'
        elif ext == 'mp4':
            merged_ext = 'mp4'
        elif ext == 'ts':
            if has_ffmpeg_installed():
                merged_ext = 'mkv'
            else:
                merged_ext = 'ts'
    return '%s.%s' % (title, merged_ext)

def download_urls(urls, title, ext, total_size, output_dir='.', refer=None, merge=True, faker=False, headers = {}, **kwargs):
    assert urls
    if json_output:
        json_output_.download_urls(urls=urls, title=title, ext=ext, total_size=total_size, refer=refer)
        return
    if dry_run:
        print('Real URLs:\n%s' % '\n'.join(urls))
        return

    if player:
        launch_player(player, urls)
        return

    if not total_size:
        try:
            total_size = urls_size(urls, faker=faker, headers=headers)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout)
            pass

    title = tr(get_filename(title))
    output_filename = get_output_filename(urls, title, ext, output_dir, merge)
    output_filepath = os.path.join(output_dir, output_filename)

    if total_size:
        if not force and os.path.exists(output_filepath) and os.path.getsize(output_filepath) >= total_size * 0.9:
            print('Skipping %s: file already exists' % output_filepath)
            print()
            return
        bar = SimpleProgressBar(total_size, len(urls))
    else:
        bar = PiecesProgressBar(total_size, len(urls))

    if len(urls) == 1:
        url = urls[0]
        print('Downloading %s ...' % tr(output_filename))
        bar.update()
        url_save(url, output_filepath, bar, refer = refer, faker = faker, headers = headers)
        bar.done()
    else:
        parts = []
        print('Downloading %s.%s ...' % (tr(title), ext))
        bar.update()
        for i, url in enumerate(urls):
            filename = '%s[%02d].%s' % (title, i, ext)
            filepath = os.path.join(output_dir, filename)
            parts.append(filepath)
            #print 'Downloading %s [%s/%s]...' % (tr(filename), i + 1, len(urls))
            bar.update_piece(i + 1)
            url_save(url, filepath, bar, refer = refer, is_part = True, faker = faker, headers = headers)
        bar.done()

        if not merge:
            print()
            return

        if 'av' in kwargs and kwargs['av']:
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_concat_av
                ret = ffmpeg_concat_av(parts, output_filepath, ext)
                print('Merged into %s' % output_filename)
                if ret == 0:
                    for part in parts: os.remove(part)

        elif ext in ['flv', 'f4v']:
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_flv_to_mp4
                    ffmpeg_concat_flv_to_mp4(parts, output_filepath)
                else:
                    from .processor.join_flv import concat_flv
                    concat_flv(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        elif ext == 'mp4':
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_mp4_to_mp4
                    ffmpeg_concat_mp4_to_mp4(parts, output_filepath)
                else:
                    from .processor.join_mp4 import concat_mp4
                    concat_mp4(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        elif ext == "ts":
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_ts_to_mkv
                    ffmpeg_concat_ts_to_mkv(parts, output_filepath)
                else:
                    from .processor.join_ts import concat_ts
                    concat_ts(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        else:
            print("Can't merge %s files" % ext)

    print()

def download_urls_chunked(urls, title, ext, total_size, output_dir='.', refer=None, merge=True, faker=False, headers = {}, **kwargs):
    assert urls
    if dry_run:
        print('Real URLs:\n%s\n' % urls)
        return

    if player:
        launch_player(player, urls)
        return

    title = tr(get_filename(title))

    filename = '%s.%s' % (title, ext)
    filepath = os.path.join(output_dir, filename)
    if total_size:
        if not force and os.path.exists(filepath[:-3] + '.mkv'):
            print('Skipping %s: file already exists' % filepath[:-3] + '.mkv')
            print()
            return
        bar = SimpleProgressBar(total_size, len(urls))
    else:
        bar = PiecesProgressBar(total_size, len(urls))

    if len(urls) == 1:
        parts = []
        url = urls[0]
        print('Downloading %s ...' % tr(filename))
        filepath = os.path.join(output_dir, filename)
        parts.append(filepath)
        url_save_chunked(url, filepath, bar, refer = refer, faker = faker, headers = headers, **kwargs)
        bar.done()

        if not merge:
            print()
            return
        if ext == 'ts':
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_convert_ts_to_mkv
                if ffmpeg_convert_ts_to_mkv(parts, os.path.join(output_dir, title + '.mkv')):
                    for part in parts:
                        os.remove(part)
                else:
                    os.remove(os.path.join(output_dir, title + '.mkv'))
            else:
                print('No ffmpeg is found. Conversion aborted.')
        else:
            print("Can't convert %s files" % ext)
    else:
        parts = []
        print('Downloading %s.%s ...' % (tr(title), ext))
        for i, url in enumerate(urls):
            filename = '%s[%02d].%s' % (title, i, ext)
            filepath = os.path.join(output_dir, filename)
            parts.append(filepath)
            #print 'Downloading %s [%s/%s]...' % (tr(filename), i + 1, len(urls))
            bar.update_piece(i + 1)
            url_save_chunked(url, filepath, bar, refer = refer, is_part = True, faker = faker, headers = headers)
        bar.done()

        if not merge:
            print()
            return
        if ext == 'ts':
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_concat_ts_to_mkv
                if ffmpeg_concat_ts_to_mkv(parts, os.path.join(output_dir, title + '.mkv')):
                    for part in parts:
                        os.remove(part)
                else:
                    os.remove(os.path.join(output_dir, title + '.mkv'))
            else:
                print('No ffmpeg is found. Merging aborted.')
        else:
            print("Can't merge %s files" % ext)

    print()

def download_rtmp_url(url,title, ext,params={}, total_size=0, output_dir='.', refer=None, merge=True, faker=False):
    assert url
    if dry_run:
        print('Real URL:\n%s\n' % [url])
        if params.get("-y",False): #None or unset ->False
            print('Real Playpath:\n%s\n' % [params.get("-y")])
        return

    if player:
        from .processor.rtmpdump import play_rtmpdump_stream
        play_rtmpdump_stream(player, url, params)
        return

    from .processor.rtmpdump import has_rtmpdump_installed, download_rtmpdump_stream
    assert has_rtmpdump_installed(), "RTMPDump not installed."
    download_rtmpdump_stream(url,  title, ext,params, output_dir)

def download_url_ffmpeg(url,title, ext,params={}, total_size=0, output_dir='.', refer=None, merge=True, faker=False):
    assert url
    if dry_run:
        print('Real URL:\n%s\n' % [url])
        if params.get("-y",False): #None or unset ->False
            print('Real Playpath:\n%s\n' % [params.get("-y")])
        return

    if player:
        launch_player(player, [url])
        return

    from .processor.ffmpeg import has_ffmpeg_installed, ffmpeg_download_stream
    assert has_ffmpeg_installed(), "FFmpeg not installed."

    global output_filename
    if output_filename:
        dotPos = output_filename.rfind(".")
        title = output_filename[:dotPos]
        ext = output_filename[dotPos+1:]

    title = tr(get_filename(title))

    ffmpeg_download_stream(url, title, ext, params, output_dir)

def playlist_not_supported(name):
    def f(*args, **kwargs):
        raise NotImplementedError('Playlist is not supported for ' + name)
    return f

def print_info(site_info, title, type, size):
    if json_output:
        json_output_.print_info(site_info=site_info, title=title, type=type, size=size)
        return
    if type:
        type = type.lower()
    if type in ['3gp']:
        type = 'video/3gpp'
    elif type in ['asf', 'wmv']:
        type = 'video/x-ms-asf'
    elif type in ['flv', 'f4v']:
        type = 'video/x-flv'
    elif type in ['mkv']:
        type = 'video/x-matroska'
    elif type in ['mp3']:
        type = 'audio/mpeg'
    elif type in ['mp4']:
        type = 'video/mp4'
    elif type in ['mov']:
        type = 'video/quicktime'
    elif type in ['ts']:
        type = 'video/MP2T'
    elif type in ['webm']:
        type = 'video/webm'

    elif type in ['jpg']:
        type = 'image/jpeg'
    elif type in ['png']:
        type = 'image/png'
    elif type in ['gif']:
        type = 'image/gif'

    if type in ['video/3gpp']:
        type_info = "3GPP multimedia file (%s)" % type
    elif type in ['video/x-flv', 'video/f4v']:
        type_info = "Flash video (%s)" % type
    elif type in ['video/mp4', 'video/x-m4v']:
        type_info = "MPEG-4 video (%s)" % type
    elif type in ['video/MP2T']:
        type_info = "MPEG-2 transport stream (%s)" % type
    elif type in ['video/webm']:
        type_info = "WebM video (%s)" % type
    #elif type in ['video/ogg']:
    #    type_info = "Ogg video (%s)" % type
    elif type in ['video/quicktime']:
        type_info = "QuickTime video (%s)" % type
    elif type in ['video/x-matroska']:
        type_info = "Matroska video (%s)" % type
    #elif type in ['video/x-ms-wmv']:
    #    type_info = "Windows Media video (%s)" % type
    elif type in ['video/x-ms-asf']:
        type_info = "Advanced Systems Format (%s)" % type
    #elif type in ['video/mpeg']:
    #    type_info = "MPEG video (%s)" % type
    elif type in ['audio/mp4']:
        type_info = "MPEG-4 audio (%s)" % type
    elif type in ['audio/mpeg']:
        type_info = "MP3 (%s)" % type

    elif type in ['image/jpeg']:
        type_info = "JPEG Image (%s)" % type
    elif type in ['image/png']:
        type_info = "Portable Network Graphics (%s)" % type
    elif type in ['image/gif']:
        type_info = "Graphics Interchange Format (%s)" % type

    else:
        type_info = "Unknown type (%s)" % type

    maybe_print("Site:      ", site_info)
    maybe_print("Title:     ", unescape_html(tr(title)))
    print("Type:      ", type_info)
    print("Size:      ", round(size / 1048576, 2), "MiB (" + str(size) + " Bytes)")
    print()

def mime_to_container(mime):
    mapping = {
        'video/3gpp': '3gp',
        'video/mp4': 'mp4',
        'video/webm': 'webm',
        'video/x-flv': 'flv',
    }
    if mime in mapping:
        return mapping[mime]
    else:
        return mime.split('/')[1]

def parse_host(host):
    """Parses host name and port number from a string.
    """
    if re.match(r'^(\d+)$', host) is not None:
        return ("0.0.0.0", int(host))
    if re.match(r'^(\w+)://', host) is None:
        host = "//" + host
    o = parse.urlparse(host)
    hostname = o.hostname or "0.0.0.0"
    port = o.port or 0
    return (hostname, port)

def set_proxy(proxy):
    proxy_handler = request.ProxyHandler({
        'http': '%s:%s' % proxy,
        'https': '%s:%s' % proxy,
    })
    opener = request.build_opener(proxy_handler)
    request.install_opener(opener)

def unset_proxy():
    proxy_handler = request.ProxyHandler({})
    opener = request.build_opener(proxy_handler)
    request.install_opener(opener)

# DEPRECATED in favor of set_proxy() and unset_proxy()
def set_http_proxy(proxy):
    if proxy == None: # Use system default setting
        proxy_support = request.ProxyHandler()
    elif proxy == '': # Don't use any proxy
        proxy_support = request.ProxyHandler({})
    else: # Use proxy
        proxy_support = request.ProxyHandler({'http': '%s' % proxy, 'https': '%s' % proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

def print_more_compatible(*args, **kwargs):
    import builtins as __builtin__
    """Overload default print function as py (<3.3) does not support 'flush' keyword.
    Although the function name can be same as print to get itself overloaded automatically,
    I'd rather leave it with a different name and only overload it when importing to make less confusion. """
    # nothing happens on py3.3 and later
    if sys.version_info[:2] >= (3, 3):
        return __builtin__.print(*args, **kwargs)

    # in lower pyver (e.g. 3.2.x), remove 'flush' keyword and flush it as requested
    doFlush = kwargs.pop('flush', False)
    ret = __builtin__.print(*args, **kwargs)
    if doFlush:
        kwargs.get('file', sys.stdout).flush()
    return ret



def download_main(download, download_playlist, urls, playlist, **kwargs):
    for url in urls:
        if url.startswith('https://'):
            url = url[8:]
        if not url.startswith('http://'):
            url = 'http://' + url

        if playlist:
            download_playlist(url, **kwargs)
        else:
            download(url, **kwargs)

def script_main(script_name, download, download_playlist, **kwargs):
    def version():
        log.i('version %s, a tiny downloader that scrapes the web.'
              % get_version(kwargs['repo_path']
            if 'repo_path' in kwargs else __version__))

    logging.basicConfig(format='[%(levelname)s] %(message)s')

    help = 'Usage: %s [OPTION]... [URL]...\n\n' % script_name
    help += '''Startup options:
    -V | --version                      Print version and exit.
    -h | --help                         Print help and exit.
    \n'''
    help += '''Dry-run options: (no actual downloading)
    -i | --info                         Print extracted information.
    -u | --url                          Print extracted information with URLs.
         --json                         Print extracted URLs in JSON format.
    \n'''
    help += '''Download options:
    -n | --no-merge                     Do not merge video parts.
         --no-caption                   Do not download captions.
                                        (subtitles, lyrics, danmaku, ...)
    -f | --force                        Force overwriting existed files.
    -F | --format <STREAM_ID>           Set video format to STREAM_ID.
    -O | --output-filename <FILE>       Set output filename.
    -o | --output-dir <PATH>            Set output directory.
    -p | --player <PLAYER [OPTIONS]>    Stream extracted URL to a PLAYER.
    -c | --cookies <COOKIES_FILE>       Load cookies.txt or cookies.sqlite.
    -x | --http-proxy <HOST:PORT>       Use an HTTP proxy for downloading.
    -y | --extractor-proxy <HOST:PORT>  Use an HTTP proxy for extracting only.
         --no-proxy                     Never use a proxy.
    -s | --socks-proxy <HOST:PORT>      Use an SOCKS5 proxy for downloading.
    -t | --timeout <SECONDS>            Set socket timeout.
    -d | --debug                        Show traceback and other debug info.
    '''

    short_opts = 'Vhfiuc:ndF:O:o:p:x:y:s:t:'
    opts = ['version', 'help', 'force', 'info', 'url', 'cookies', 'no-caption', 'no-merge', 'no-proxy', 'debug', 'json', 'format=', 'stream=', 'itag=', 'output-filename=', 'output-dir=', 'player=', 'http-proxy=', 'socks-proxy=', 'extractor-proxy=', 'lang=', 'timeout=']
    if download_playlist:
        short_opts = 'l' + short_opts
        opts = ['playlist'] + opts

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
    except getopt.GetoptError as err:
        log.e(err)
        log.e("try 'you-get --help' for more options")
        sys.exit(2)

    global force
    global dry_run
    global json_output
    global player
    global extractor_proxy
    global cookies
    global output_filename

    info_only = False
    playlist = False
    caption = True
    merge = True
    stream_id = None
    lang = None
    output_dir = '.'
    proxy = None
    socks_proxy = None
    extractor_proxy = None
    traceback = False
    timeout = 600
    for o, a in opts:
        if o in ('-V', '--version'):
            version()
            sys.exit()
        elif o in ('-h', '--help'):
            version()
            print(help)
            sys.exit()
        elif o in ('-f', '--force'):
            force = True
        elif o in ('-i', '--info'):
            info_only = True
        elif o in ('-u', '--url'):
            dry_run = True
        elif o in ('--json', ):
            json_output = True
            # to fix extractors not use VideoExtractor
            dry_run = True
            info_only = False
        elif o in ('-c', '--cookies'):
            try:
                cookies = cookiejar.MozillaCookieJar(a)
                cookies.load()
            except:
                import sqlite3
                cookies = cookiejar.MozillaCookieJar()
                con = sqlite3.connect(a)
                cur = con.cursor()
                try:
                    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
                    for item in cur.fetchall():
                        c = cookiejar.Cookie(0, item[4], item[5],
                                             None, False,
                                             item[0],
                                             item[0].startswith('.'),
                                             item[0].startswith('.'),
                                             item[1], False,
                                             item[2],
                                             item[3], item[3]=="",
                                             None, None, {})
                        cookies.set_cookie(c)
                except: pass
                # TODO: Chromium Cookies
                # SELECT host_key, path, secure, expires_utc, name, encrypted_value FROM cookies
                # http://n8henrie.com/2013/11/use-chromes-cookies-for-easier-downloading-with-python-requests/

        elif o in ('-l', '--playlist'):
            playlist = True
        elif o in ('--no-caption',):
            caption = False
        elif o in ('-n', '--no-merge'):
            merge = False
        elif o in ('--no-proxy',):
            proxy = ''
        elif o in ('-d', '--debug'):
            traceback = True
            # Set level of root logger to DEBUG
            logging.getLogger().setLevel(logging.DEBUG)
        elif o in ('-F', '--format', '--stream', '--itag'):
            stream_id = a
        elif o in ('-O', '--output-filename'):
            output_filename = a
        elif o in ('-o', '--output-dir'):
            output_dir = a
        elif o in ('-p', '--player'):
            player = a
            caption = False
        elif o in ('-x', '--http-proxy'):
            proxy = a
        elif o in ('-s', '--socks-proxy'):
            socks_proxy = a
        elif o in ('-y', '--extractor-proxy'):
            extractor_proxy = a
        elif o in ('--lang',):
            lang = a
        elif o in ('-t', '--timeout'):
            timeout = int(a)
        else:
            log.e("try 'you-get --help' for more options")
            sys.exit(2)
    if not args:
        print(help)
        sys.exit()

    if (socks_proxy):
        try:
            import socket
            import socks
            socks_proxy_addrs = socks_proxy.split(':')
            socks.set_default_proxy(socks.SOCKS5,
                                    socks_proxy_addrs[0],
                                    int(socks_proxy_addrs[1]))
            socket.socket = socks.socksocket
            def getaddrinfo(*args):
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
            socket.getaddrinfo = getaddrinfo
        except ImportError:
            log.w('Error importing PySocks library, socks proxy ignored.'
                'In order to use use socks proxy, please install PySocks.')
    else:
        import socket
        set_http_proxy(proxy)

    socket.setdefaulttimeout(timeout)

    try:
        if stream_id:
            if not extractor_proxy:
                download_main(download, download_playlist, args, playlist, stream_id=stream_id, output_dir=output_dir, merge=merge, info_only=info_only, json_output=json_output, caption=caption)
            else:
                download_main(download, download_playlist, args, playlist, stream_id=stream_id, extractor_proxy=extractor_proxy, output_dir=output_dir, merge=merge, info_only=info_only, json_output=json_output, caption=caption)
        else:
            if not extractor_proxy:
                download_main(download, download_playlist, args, playlist, output_dir=output_dir, merge=merge, info_only=info_only, json_output=json_output, caption=caption)
            else:
                download_main(download, download_playlist, args, playlist, extractor_proxy=extractor_proxy, output_dir=output_dir, merge=merge, info_only=info_only, json_output=json_output, caption=caption)
    except KeyboardInterrupt:
        if traceback:
            raise
        else:
            sys.exit(1)
    except UnicodeEncodeError:
        log.e('[error] oops, the current environment does not seem to support Unicode.')
        log.e('please set it to a UTF-8-aware locale first,')
        log.e('so as to save the video (with some Unicode characters) correctly.')
        log.e('you can do it like this:')
        log.e('    (Windows)    % chcp 65001 ')
        log.e('    (Linux)      $ LC_CTYPE=en_US.UTF-8')
        sys.exit(1)
    except Exception:
        if not traceback:
            log.e('[error] oops, something went wrong.')
            log.e('don\'t panic, c\'est la vie. please try the following steps:')
            log.e('  (1) Rule out any network problem.')
            log.e('  (2) Make sure you-get is up-to-date.')
            log.e('  (3) Check if the issue is already known, on')
            log.e('        https://github.com/soimort/you-get/wiki/Known-Bugs')
            log.e('        https://github.com/soimort/you-get/issues')
            log.e('  (4) Run the command with \'--debug\' option,')
            log.e('      and report this issue with the full output.')
        else:
            version()
            log.i(args)
            raise
        sys.exit(1)

def google_search(url):
    keywords = r1(r'https?://(.*)', url)
    url = 'https://www.google.com/search?tbm=vid&q=%s' % parse.quote(keywords)
    page = get_content(url, headers=fake_headers)
    videos = re.findall(r'<a href="(https?://[^"]+)" onmousedown="[^"]+">([^<]+)<', page)
    vdurs = re.findall(r'<span class="vdur _dwc">([^<]+)<', page)
    durs = [r1(r'(\d+:\d+)', unescape_html(dur)) for dur in vdurs]
    print("Google Videos search:")
    for v in zip(videos, durs):
        print("- video:  %s [%s]" % (unescape_html(v[0][1]),
                                     v[1] if v[1] else '?'))
        print("# you-get %s" % log.sprint(v[0][0], log.UNDERLINE))
        print()
    print("Best matched result:")
    return(videos[0][0])

def url_to_module(url):
    try:
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except:
        url = google_search(url)
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)

    if video_host.endswith('.com.cn'):
        video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domain, 'unsupported url: ' + url

    k = r1(r'([^.]+)', domain)
    if k in SITES:
        return import_module('.'.join(['you_get', 'extractors', SITES[k]])), url
    else:
        import http.client
        conn = http.client.HTTPConnection(video_host)
        conn.request("HEAD", video_url, headers=fake_headers)
        res = conn.getresponse()
        location = res.getheader('location')
        if location and location != url and not location.startswith('/'):
            return url_to_module(location)
        else:
            return import_module('you_get.extractors.universal'), url

def any_download(url, **kwargs):
    m, url = url_to_module(url)
    m.download(url, **kwargs)

def any_download_playlist(url, **kwargs):
    m, url = url_to_module(url)
    m.download_playlist(url, **kwargs)

def main(**kwargs):
    script_main('you-get', any_download, any_download_playlist, **kwargs)
