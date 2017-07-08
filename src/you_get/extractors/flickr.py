#!/usr/bin/env python

__all__ = ['flickr_download_main']

from ..common import *

import json

pattern_url_photoset = r'https?://www\.flickr\.com/photos/.+/(?:(?:sets)|(?:albums))?/([^/]+)'
pattern_url_photostream = r'https?://www\.flickr\.com/photos/([^/]+)(?:/|(?:/page))?$'
pattern_url_single_photo = r'https?://www\.flickr\.com/photos/[^/]+/(\d+)'
pattern_url_gallery = r'https?://www\.flickr\.com/photos/[^/]+/galleries/(\d+)'
pattern_url_group = r'https?://www\.flickr\.com/groups/([^/]+)'
pattern_url_favorite = r'https?://www\.flickr\.com/photos/([^/]+)/favorites'

pattern_inline_title = r'<title>([^<]*)</title>'
pattern_inline_api_key = r'api\.site_key\s*=\s*"([^"]+)"'
pattern_inline_img_url = r'"url":"([^"]+)","key":"[^"]+"}}'
pattern_inline_NSID = r'"nsid"\s*:\s*"([^"]+)"'
pattern_inline_video_mark = r'("mediaType":"video")'

# (api_key, method, ext, page)
tmpl_api_call = (
    'https://api.flickr.com/services/rest?'
    '&format=json&nojsoncallback=1'
    # UNCOMMENT FOR TESTING
    #'&per_page=5'
    '&per_page=500'
    # this parameter CANNOT take control of 'flickr.galleries.getPhotos'
    # though the doc said it should.
    # it's always considered to be 500
    '&api_key=%s'
    '&method=flickr.%s'
    '&extras=url_sq,url_q,url_t,url_s,url_n,url_m,url_z,url_c,url_l,url_h,url_k,url_o,media'
    '%s&page=%d'
)

tmpl_api_call_video_info = (
    'https://api.flickr.com/services/rest?'
    '&format=json&nojsoncallback=1'
    '&method=flickr.video.getStreamInfo'
    '&api_key=%s'
    '&photo_id=%s'
    '&secret=%s'
)

tmpl_api_call_photo_info = (
    'https://api.flickr.com/services/rest?'
    '&format=json&nojsoncallback=1'
    '&method=flickr.photos.getInfo'
    '&api_key=%s'
    '&photo_id=%s'
)

# looks that flickr won't return urls for all sizes
# we required in 'extras field without a acceptable header
dummy_header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}
def get_content_headered(url):
    return get_content(url, dummy_header)

def get_photoset_id(url, page):
    return match1(url, pattern_url_photoset)

def get_photo_id(url, page):
    return match1(url, pattern_url_single_photo)

def get_gallery_id(url, page):
    return match1(url, pattern_url_gallery)

def get_api_key(page):
    match = match1(page, pattern_inline_api_key)
    # this happens only when the url points to a gallery page
    # that contains no inline api_key(and never makes xhr api calls)
    # in fact this might be a better approch for getting a temporary api key
    # since there's no place for a user to add custom infomation that may
    # misguide the regex in the homepage
    if not match:
        return match1(get_html('https://flickr.com'), pattern_inline_api_key)
    return match

def get_NSID(url, page):
    return match1(page, pattern_inline_NSID)

# [
# (
#   regex_match_url,
#   remote_api_method,
#   additional_query_parameter_for_method,
#   parser_for_additional_parameter,
#   field_where_photourls_are_saved
# )
# ]
url_patterns = [
    # www.flickr.com/photos/{username|NSID}/sets|albums/{album-id}
    (
        pattern_url_photoset,
        'photosets.getPhotos',
        'photoset_id',
        get_photoset_id,
        'photoset'
    ),
    # www.flickr.com/photos/{username|NSID}/{pageN}?
    (
        pattern_url_photostream,
        # according to flickr api documentation, this method needs to be
        # authenticated in order to filter photo visible to the calling user
        # but it seems works fine anonymously as well
        'people.getPhotos',
        'user_id',
        get_NSID,
        'photos'
    ),
    # www.flickr.com/photos/{username|NSID}/galleries/{gallery-id}
    (
        pattern_url_gallery,
        'galleries.getPhotos',
        'gallery_id',
        get_gallery_id,
        'photos'
    ),
    # www.flickr.com/groups/{groupname|groupNSID}/
    (
        pattern_url_group,
        'groups.pools.getPhotos',
        'group_id',
        get_NSID,
        'photos'
    ),
    # www.flickr.com/photos/{username|NSID}/favorites/*
    (
        pattern_url_favorite,
        'favorites.getList',
        'user_id',
        get_NSID,
        'photos'
    )
]

def flickr_download_main(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    urls = None
    size = 'o' # works for collections only
    title = None
    if 'stream_id' in kwargs:
        size = kwargs['stream_id']
    if match1(url, pattern_url_single_photo):
        url, title = get_single_photo_url(url)
        urls = [url]
    else:
        urls, title = fetch_photo_url_list(url, size)
    index = 0
    for url in urls:
        mime, ext, size = url_info(url)
        print_info('Flickr.com', title, mime, size)
        if not info_only:
            suffix = '[%d]' % index
            download_urls([url], title + suffix, ext, False, output_dir, None, False, False)
            index = index + 1

def fetch_photo_url_list(url, size):
    for pattern in url_patterns:
        # FIXME: fix multiple matching since the match group is dropped
        if match1(url, pattern[0]):
            return fetch_photo_url_list_impl(url, size, *pattern[1:])
    raise NotImplementedError('Flickr extractor is not supported for %s.' % url)

def fetch_photo_url_list_impl(url, size, method, id_field, id_parse_func, collection_name):
    page = get_html(url)
    api_key = get_api_key(page)
    ext_field = ''
    if id_parse_func:
        ext_field = '&%s=%s' % (id_field, id_parse_func(url, page))
    page_number = 1
    urls = []
    while True:
        call_url = tmpl_api_call % (api_key, method, ext_field, page_number)
        photoset = json.loads(get_content_headered(call_url))[collection_name]
        pagen = photoset['page']
        pages = photoset['pages']
        for info in photoset['photo']:
            url = get_url_of_largest(info, api_key, size)
            urls.append(url)
        page_number = page_number + 1
        # the typeof 'page' and 'pages' may change in different methods
        if str(pagen) == str(pages):
            break
    return urls, match1(page, pattern_inline_title)

# image size suffixes used in inline json 'key' field
# listed in descending order
size_suffixes = ['o', 'k', 'h', 'l', 'c', 'z', 'm', 'n', 's', 't', 'q', 'sq']

def get_orig_video_source(api_key, pid, secret):
    parsed = json.loads(get_content_headered(tmpl_api_call_video_info % (api_key, pid, secret)))
    for stream in parsed['streams']['stream']:
        if stream['type'] == 'orig':
            return stream['_content'].replace('\\', '')
    return None

def get_url_of_largest(info, api_key, size):
    if info['media'] == 'photo':
        sizes = size_suffixes
        if size in sizes:
            sizes = sizes[sizes.index(size):]
        for suffix in sizes:
            if 'url_' + suffix in info:
                return info['url_' + suffix].replace('\\', '')
        return None
    else:
        return get_orig_video_source(api_key, info['id'], info['secret'])

def get_single_photo_url(url):
    page = get_html(url)
    pid = get_photo_id(url, page)
    title = match1(page, pattern_inline_title)
    if match1(page, pattern_inline_video_mark):
        api_key = get_api_key(page)
        reply = get_content(tmpl_api_call_photo_info % (api_key, get_photo_id(url, page)))
        secret = json.loads(reply)['photo']['secret']
        return get_orig_video_source(api_key, pid, secret), title
    #last match always has the best resolution
    match = match1(page, pattern_inline_img_url)
    return 'https:' + match.replace('\\', ''), title

site_info = "Flickr.com"
download = flickr_download_main
download_playlist = playlist_not_supported('flickr');
