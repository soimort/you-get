import os
import json

# save info from common.print_info()
last_info = None

def output(video_extractor, pretty_print=True, tofile=False):
    ve = video_extractor
    out = {}
    out['url'] = ve.url
    out['title'] = ve.title
    out['site'] = ve.name
    out['streams'] = ve.streams
    try:
        if ve.audiolang:
            out['audiolang'] = ve.audiolang
    except AttributeError:
        pass
    if pretty_print:
        json_content = json.dumps(out, indent=4, sort_keys=True, ensure_ascii=False)
    else:
        json_content = json.dumps(out)
    if tofile:
        jsondir = 'json'
        if not os.path.exists(jsondir):
            os.mkdir(jsondir)
        filename = '%s/%03d_%s.json' % (jsondir, ve.index, ve.title)
        f = open(filename, 'wb')
        _output = f.write
        json_content = json_content.encode('utf8')
    else:
        _output = print
    _output(json_content)

# a fake VideoExtractor object to save info
class VideoExtractor(object):
    pass

def print_info(site_info=None, title=None, type=None, size=None):
    global last_info
    # create a VideoExtractor and save info for download_urls()
    ve = VideoExtractor()
    last_info = ve
    ve.name = site_info
    ve.title = title
    ve.url = None

def download_urls(urls=None, title=None, ext=None, total_size=None, refer=None):
    ve = last_info
    if not ve:
        ve = VideoExtractor()
        ve.name = ''
        ve.url = urls
        ve.title=title
    # save download info in streams
    stream = {}
    stream['container'] = ext
    stream['size'] = total_size
    stream['src'] = urls
    if refer:
        stream['refer'] = refer
    stream['video_profile'] = '__default__'
    ve.streams = {}
    ve.streams['__default__'] = stream
    output(ve)

