
import json

# save info from common.print_info()
last_info = None


def output(video_extractor, pretty_print=True):
    ve = video_extractor
    out = {'url': ve.url, 'title': ve.title, 'site': ve.name, 'streams': ve.streams}
    if pretty_print:
        print(json.dumps(out, indent=4, sort_keys=True, ensure_ascii=False))
    else:
        print(json.dumps(out))


class VideoExtractor(object):
    """
    a fake VideoExtractor object to save info
    """
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
    # save download info in streams
    stream = {'container': ext, 'size': total_size, 'src': urls}
    if refer:
        stream['refer'] = refer
    stream['video_profile'] = '__default__'
    ve.streams = {'__default__': stream}
    output(ve)

