#!/usr/bin/env python

import getopt
import json
import locale
import os
import re
import sys
from urllib import request, parse

__version__ = "0.2.8"

dry_run = False
force = False

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1'
}

if sys.stdout.isatty():
    default_encoding = sys.stdout.encoding.lower()
else:
    default_encoding = locale.getpreferredencoding().lower()

def tr(s):
    try:
        s.encode(default_encoding)
        return s
    except:
        return str(s.encode('utf-8'))[2:-1]

def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

def r1_of(patterns, text):
    for p in patterns:
        x = r1(p, text)
        if x:
            return x

def unicodize(text):
    return re.sub(r'\\u([0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])', lambda x: chr(int(x.group(0)[2:], 16)), text)

def escape_file_path(path):
    path = path.replace('/', '-')
    path = path.replace('\\', '-')
    path = path.replace('*', '-')
    path = path.replace('?', '-')
    return path

def unescape_html(html):
    from html import parser
    html = parser.HTMLParser().unescape(html)
    html = re.sub(r'&#(\d+);', lambda x: chr(int(x.group(1))), html)
    return html

def ungzip(s):
    from io import BytesIO
    import gzip
    buffer = BytesIO(s)
    f = gzip.GzipFile(fileobj = buffer)
    return f.read()

def undeflate(s):
    import zlib
    return zlib.decompress(s, -zlib.MAX_WBITS)

def get_response(url, faker = False):
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

def get_html(url, encoding = None, faker = False):
    content = get_response(url, faker).data
    return str(content, 'utf-8', 'ignore')

def get_decoded_html(url, faker = False):
    response = get_response(url, faker)
    data = response.data
    charset = r1(r'charset=([\w-]+)', response.headers['content-type'])
    if charset:
        return data.decode(charset)
    else:
        return data

def url_size(url, faker = False):
    if faker:
        response = request.urlopen(request.Request(url, headers = fake_headers), None)
    else:
        response = request.urlopen(url)
    
    size = int(response.headers['content-length'])
    return size

def urls_size(urls):
    return sum(map(url_size, urls))

def url_info(url, faker = False):
    if faker:
        response = request.urlopen(request.Request(url, headers = fake_headers), None)
    else:
        response = request.urlopen(request.Request(url))
    
    headers = response.headers
    
    type = headers['content-type']
    mapping = {
        'video/3gpp': '3gp',
        'video/f4v': 'flv',
        'video/mp4': 'mp4',
        'video/MP2T': 'ts',
        'video/webm': 'webm',
        'video/x-flv': 'flv'
    }
    if type in mapping:
        ext = mapping[type]
    else:
        ext = None
    
    size = int(headers['content-length'])
    
    return type, ext, size

def url_locations(urls, faker = False):
    locations = []
    for url in urls:
        if faker:
            response = request.urlopen(request.Request(url, headers = fake_headers), None)
        else:
            response = request.urlopen(request.Request(url))
        
        locations.append(response.url)
    return locations

def url_save(url, filepath, bar, refer = None, is_part = False, faker = False):
    file_size = url_size(url, faker = faker)
    
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
    
    if received < file_size:
        if faker:
            headers = fake_headers
        else:
            headers = {}
        if received:
            headers['Range'] = 'bytes=' + str(received) + '-'
        if refer:
            headers['Referer'] = refer
        
        response = request.urlopen(request.Request(url, headers = headers), None)
        
        if file_size != received + int(response.headers['content-length']):
            received = 0
            open_mode = 'wb'
        
        with open(temp_filepath, open_mode) as output:
            while True:
                buffer = response.read(1024 * 256)
                if not buffer:
                    if received == file_size: # Download finished
                        break
                    else: # Unexpected termination. Retry request
                        headers['Range'] = 'bytes=' + str(received) + '-'
                        response = request.urlopen(request.Request(url, headers = headers), None)
                output.write(buffer)
                received += len(buffer)
                if bar:
                    bar.update_received(len(buffer))
    
    assert received == os.path.getsize(temp_filepath), '%s == %s == %s' % (received, os.path.getsize(temp_filepath))
    
    if os.access(filepath, os.W_OK):
        os.remove(filepath) # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)

def url_save_chunked(url, filepath, bar, refer = None, is_part = False, faker = False):
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
    else:
        headers = {}
    if received:
        headers['Range'] = 'bytes=' + str(received) + '-'
    if refer:
        headers['Referer'] = refer
    
    response = request.urlopen(request.Request(url, headers = headers), None)
    
    with open(temp_filepath, open_mode) as output:
        while True:
            buffer = response.read(1024 * 256)
            if not buffer:
                break
            output.write(buffer)
            received += len(buffer)
            if bar:
                bar.update_received(len(buffer))
    
    assert received == os.path.getsize(temp_filepath), '%s == %s == %s' % (received, os.path.getsize(temp_filepath))
    
    if os.access(filepath, os.W_OK):
        os.remove(filepath) # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)

class SimpleProgressBar:
    def __init__(self, total_size, total_pieces = 1):
        self.displayed = False
        self.total_size = total_size
        self.total_pieces = total_pieces
        self.current_piece = 1
        self.received = 0
        
    def update(self):
        self.displayed = True
        bar_size = 40
        percent = round(self.received * 100 / self.total_size, 1)
        if percent > 100:
            percent = 100
        dots = bar_size * int(percent) // 100
        plus = int(percent) - dots // bar_size * 100
        if plus > 0.8:
            plus = '='
        elif plus > 0.4:
            plus = '>'
        else:
            plus = ''
        bar = '=' * dots + plus
        bar = '{0:>5}% ({1:>5}/{2:<5}MB) [{3:<40}] {4}/{5}'.format(percent, round(self.received / 1048576, 1), round(self.total_size / 1048576, 1), bar, self.current_piece, self.total_pieces)
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

class PiecesProgressBar:
    def __init__(self, total_size, total_pieces = 1):
        self.displayed = False
        self.total_size = total_size
        self.total_pieces = total_pieces
        self.current_piece = 1
        self.received = 0
        
    def update(self):
        self.displayed = True
        bar = '{0:>5}%[{1:<40}] {2}/{3}'.format('?', '?' * 40, self.current_piece, self.total_pieces)
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

def download_urls(urls, title, ext, total_size, output_dir = '.', refer = None, merge = True, faker = False):
    assert urls
    if dry_run:
        print('Real URLs:\n', urls, '\n')
        return
    
    assert ext in ('3gp', 'flv', 'mp4', 'webm')
    if not total_size:
        try:
            total_size = urls_size(urls)
        except:
            import traceback
            import sys
            traceback.print_exc(file = sys.stdout)
            pass
    title = escape_file_path(title)
    filename = '%s.%s' % (title, ext)
    filepath = os.path.join(output_dir, filename)
    if total_size:
        if not force and os.path.exists(filepath) and os.path.getsize(filepath) >= total_size * 0.9:
            print('Skipping %s: file already exists' % tr(filepath))
            print()
            return
        bar = SimpleProgressBar(total_size, len(urls))
    else:
        bar = PiecesProgressBar(total_size, len(urls))
    
    if len(urls) == 1:
        url = urls[0]
        print('Downloading %s ...' % tr(filename))
        url_save(url, filepath, bar, refer = refer, faker = faker)
        bar.done()
    else:
        parts = []
        print('Downloading %s.%s ...' % (tr(title), ext))
        for i, url in enumerate(urls):
            filename = '%s[%02d].%s' % (title, i, ext)
            filepath = os.path.join(output_dir, filename)
            parts.append(filepath)
            #print 'Downloading %s [%s/%s]...' % (tr(filename), i + 1, len(urls))
            bar.update_piece(i + 1)
            url_save(url, filepath, bar, refer = refer, is_part = True, faker = faker)
        bar.done()
        
        if not merge:
            print()
            return
        if ext == 'flv':
            from .processor.join_flv import concat_flv
            concat_flv(parts, os.path.join(output_dir, title + '.flv'))
            for part in parts:
                os.remove(part)
        elif ext == 'mp4':
            try:
                from .processor.join_mp4 import concat_mp4
                concat_mp4(parts, os.path.join(output_dir, title + '.mp4'))
                for part in parts:
                    os.remove(part)
            except:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_mp4_to_mpg
                    ffmpeg_concat_mp4_to_mpg(parts, os.path.join(output_dir, title + '.mp4'))
                    for part in parts:
                        os.remove(part)
                else:
                    print('No ffmpeg is found. Merging aborted.')
        else:
            print("Can't merge %s files" % ext)
    
    print()

def download_urls_chunked(urls, title, ext, total_size, output_dir = '.', refer = None, merge = True, faker = False):
    assert urls
    if dry_run:
        print('Real URLs:\n', urls, '\n')
        return
    
    assert ext in ('ts')
    title = escape_file_path(title)
    filename = '%s.%s' % (title, 'ts')
    filepath = os.path.join(output_dir, filename)
    if total_size:
        if not force and os.path.exists(filepath[:-3] + '.mkv'):
            print('Skipping %s: file already exists' % tr(filepath[:-3] + '.mkv'))
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
        url_save_chunked(url, filepath, bar, refer = refer, faker = faker)
        bar.done()
        
        if not merge:
            print()
            return
        if ext == 'ts':
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_convert_ts_to_mkv
                ffmpeg_convert_ts_to_mkv(parts, os.path.join(output_dir, title + '.mkv'))
                for part in parts:
                    os.remove(part)
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
            url_save_chunked(url, filepath, bar, refer = refer, is_part = True, faker = faker)
        bar.done()
        
        if not merge:
            print()
            return
        if ext == 'ts':
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_concat_ts_to_mkv
                ffmpeg_concat_ts_to_mkv(parts, os.path.join(output_dir, title + '.mkv'))
                for part in parts:
                    os.remove(part)
            else:
                print('No ffmpeg is found. Merging aborted.')
        else:
            print("Can't merge %s files" % ext)
    
    print()

def playlist_not_supported(name):
    def f(*args, **kwargs):
        raise NotImplementedError('Playlist is not supported for ' + name)
    return f

def print_info(site_info, title, type, size):
    if type in ['3gp']:
        type = 'video/3gpp'
    elif type in ['flv', 'f4v']:
        type = 'video/x-flv'
    elif type in ['mp4']:
        type = 'video/mp4'
    elif type in ['ts']:
        type = 'video/MP2T'
    elif type in ['webm']:
        type = 'video/webm'
    
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
    #elif type in ['video/quicktime']:
    #    type_info = "QuickTime video (%s)" % type
    #elif type in ['video/x-matroska']:
    #    type_info = "Matroska video (%s)" % type
    #elif type in ['video/x-ms-wmv']:
    #    type_info = "Windows Media video (%s)" % type
    #elif type in ['video/mpeg']:
    #    type_info = "MPEG video (%s)" % type
    else:
        type_info = "Unknown type (%s)" % type
    
    print("Video Site:", site_info)
    print("Title:     ", tr(title))
    print("Type:      ", type_info)
    print("Size:      ", round(size / 1048576, 2), "MB (" + str(size) + " Bytes)")
    print()

def set_http_proxy(proxy):
    if proxy == None: # Use system default setting
        proxy_support = request.ProxyHandler()
    elif proxy == '': # Don't use any proxy
        proxy_support = request.ProxyHandler({})
    else: # Use proxy
        if not proxy.startswith('http://'):
            proxy = 'http://' + proxy
        proxy_support = request.ProxyHandler({'http': '%s' % proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

def download_main(download, download_playlist, urls, playlist, output_dir, merge, info_only):
    for url in urls:
        if url.startswith('https://'):
            url = url[8:]
        if not url.startswith('http://'):
            url = 'http://' + url
        
        if playlist:
            download_playlist(url, output_dir = output_dir, merge = merge, info_only = info_only)
        else:
            download(url, output_dir = output_dir, merge = merge, info_only = info_only)

def script_main(script_name, download, download_playlist = None):
    version = 'You-Get %s, a video downloader.' % __version__
    help = 'Usage: %s [OPTION]... [URL]...\n' % script_name
    help += '''\nStartup options:
    -V | --version                           Display the version and exit.
    -h | --help                              Print this help and exit.
    '''
    help += '''\nDownload options (use with URLs):
    -f | --force                             Force overwriting existed files.
    -i | --info                              Display the information of videos without downloading.
    -u | --url                               Display the real URLs of videos without downloading.
    -n | --no-merge                          Don't merge video parts.
    -o | --output-dir <PATH>                 Set the output directory for downloaded videos.
    -x | --http-proxy <PROXY-SERVER-IP:PORT> Use specific HTTP proxy for downloading.
         --no-proxy                          Don't use any proxy. (ignore $http_proxy)
         --debug                             Show traceback on KeyboardInterrupt.
    '''
    
    short_opts = 'Vhfiuno:x:'
    opts = ['version', 'help', 'force', 'info', 'url', 'no-merge', 'no-proxy', 'debug', 'output-dir=', 'http-proxy=']
    if download_playlist:
        short_opts = 'l' + short_opts
        opts = ['playlist'] + opts
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
    except getopt.GetoptError as err:
        print(err)
        print(help)
        sys.exit(2)
    
    info_only = False
    playlist = False
    merge = True
    output_dir = '.'
    proxy = None
    traceback = False
    for o, a in opts:
        if o in ('-V', '--version'):
            print(version)
            sys.exit()
        elif o in ('-h', '--help'):
            print(version)
            print(help)
            sys.exit()
        elif o in ('-f', '--force'):
            global force
            force = True
        elif o in ('-i', '--info'):
            info_only = True
        elif o in ('-u', '--url'):
            global dry_run
            dry_run = True
        elif o in ('-l', '--playlist'):
            playlist = True
        elif o in ('-n', '--no-merge'):
            merge = False
        elif o in ('--no-proxy'):
            proxy = ''
        elif o in ('--debug'):
            traceback = True
        elif o in ('-o', '--output-dir'):
            output_dir = a
        elif o in ('-x', '--http-proxy'):
            proxy = a
        else:
            print(help)
            sys.exit(1)
    if not args:
        print(help)
        sys.exit(1)
    
    set_http_proxy(proxy)
    
    if traceback:
        download_main(download, download_playlist, args, playlist, output_dir, merge, info_only)
    else:
        try:
            download_main(download, download_playlist, args, playlist, output_dir, merge, info_only)
        except KeyboardInterrupt:
            sys.exit(1)
