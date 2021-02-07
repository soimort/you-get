#!/usr/bin/env python

__all__ = ['tumblr_download']

from ..common import *
from .universal import *
from .dailymotion import dailymotion_download
from .vimeo import vimeo_download
from .vine import vine_download

def tumblr_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if re.match(r'https?://\d+\.media\.tumblr\.com/', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only)
        return

    import ssl
    ssl_context = request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)) # server requires TLS v1.2
    cookie_handler = request.HTTPCookieProcessor()
    opener = request.build_opener(ssl_context, cookie_handler)
    request.install_opener(opener)

    page = get_html(url)
    form_key = match1(page, r'id="tumblr_form_key" content="([^"]+)"')
    if form_key is not None:
        # bypass GDPR consent page
        referer = 'https://www.tumblr.com/privacy/consent?redirect=%s' % parse.quote_plus(url)
        post_content('https://www.tumblr.com/svc/privacy/consent',
                     headers={
                         'Content-Type': 'application/json',
                         'User-Agent': fake_headers['User-Agent'],
                         'Referer': referer,
                         'X-tumblr-form-key': form_key,
                         'X-Requested-With': 'XMLHttpRequest'
                     },
                     post_data_raw='{"eu_resident":true,"gdpr_is_acceptable_age":true,"gdpr_consent_core":true,"gdpr_consent_first_party_ads":true,"gdpr_consent_third_party_ads":true,"gdpr_consent_search_history":true,"redirect_to":"%s","gdpr_reconsent":false}' % url)
        page = get_html(url, faker=True)

    html = parse.unquote(page).replace('\/', '/')
    feed = r1(r'<meta property="og:type" content="tumblr-feed:(\w+)" />', html)

    if feed in ['photo', 'photoset', 'entry'] or feed is None:
        # try to extract photos
        page_title = r1(r'<meta name="description" content="([^"\n]+)', html) or \
                     r1(r'<meta property="og:description" content="([^"\n]+)', html) or \
                     r1(r'<title>([^<\n]*)', html)
        urls = re.findall(r'(https?://[^;"&]+/tumblr_[^;"&]+_\d+\.jpg)', html) +\
               re.findall(r'(https?://[^;"&]+/tumblr_[^;"&]+_\d+\.png)', html) +\
               re.findall(r'(https?://[^;"&]+/tumblr_[^;"&]+_\d+\.gif)', html) +\
               re.findall(r'(https?://\d+\.media\.tumblr\.com/[^;"&]+/s\d+x\d+/[^;"&]+\.jpg)', html) +\
               re.findall(r'(https?://\d+\.media\.tumblr\.com/[^;"&]+/s\d+x\d+/[^;"&]+\.png)', html) +\
               re.findall(r'(https?://\d+\.media\.tumblr\.com/[^;"&]+/s\d+x\d+/[^;"&]+\.gif)', html)

        tuggles = {}
        for url in urls:
            if url.endswith('.gif'):
                hd_url = url
            elif url.endswith('.jpg'):
                hd_url = url  # FIXME: decide actual quality # r1(r'(.+)_\d+\.jpg$', url) + '_1280.jpg'
            elif url.endswith('.png'):
                hd_url = url  # FIXME: decide actual quality # r1(r'(.+)_\d+\.png$', url) + '_1280.png'
            else:
                continue
            filename = parse.unquote(hd_url.split('/')[-1])
            title = '.'.join(filename.split('.')[:-1])
            tumblr_id = r1(r'^tumblr_(.+)_\d+$', title) or title
            try:
                quality = int(r1(r'^tumblr_.+_(\d+)$', title))
            except:
                quality = int(r1(r'/s(\d+)x\d+/', hd_url))
            ext = filename.split('.')[-1]

            try:
                size = int(get_head(hd_url)['Content-Length'])
                if tumblr_id not in tuggles or tuggles[tumblr_id]['quality'] < quality:
                    tuggles[tumblr_id] = {
                        'title': title,
                        'url': hd_url,
                        'quality': quality,
                        'ext': ext,
                        'size': size,
                    }
            except: pass

        if tuggles:
            size = sum([tuggles[t]['size'] for t in tuggles])
            print_info(site_info, page_title, None, size)

            if not info_only:
                for t in tuggles:
                    title = tuggles[t]['title']
                    ext = tuggles[t]['ext']
                    size = tuggles[t]['size']
                    url = tuggles[t]['url']
                    print_info(site_info, title, ext, size)
                    download_urls([url], title, ext, size,
                                  output_dir=output_dir)
            return

    # feed == 'audio' or feed == 'video' or feed is None
    # try to extract video / audio
    real_url = r1(r'source src=\\x22([^\\]+)\\', html)
    if not real_url:
        real_url = r1(r'audio_file=([^&]+)&', html)
        if real_url:
            real_url = real_url + '?plead=please-dont-download-this-or-our-lawyers-wont-let-us-host-audio'
    if not real_url:
        real_url = r1(r'<source src="([^"]*)"', html)
    if not real_url:
        iframe_url = r1(r'<[^>]+tumblr_video_container[^>]+><iframe[^>]+src=[\'"]([^\'"]*)[\'"]', html)

        if iframe_url is None:
            universal_download(url, output_dir, merge=merge, info_only=info_only, **kwargs)
            return

        if iframe_url:
            iframe_html = get_content(iframe_url, headers=fake_headers)
            real_url = r1(r'<video[^>]*>[\n ]*<source[^>]+src=[\'"]([^\'"]*)[\'"]', iframe_html)
        else:
            iframe_url = r1(r'<iframe[^>]+src=[\'"]([^\'"]*)[\'"]', html)
            if iframe_url[:2] == '//': iframe_url = 'http:' + iframe_url
            if re.search(r'player\.vimeo\.com', iframe_url):
                vimeo_download(iframe_url, output_dir, merge=merge, info_only=info_only,
                               referer='http://tumblr.com/', **kwargs)
                return
            elif re.search(r'dailymotion\.com', iframe_url):
                dailymotion_download(iframe_url, output_dir, merge=merge, info_only=info_only, **kwargs)
                return
            elif re.search(r'vine\.co', iframe_url):
                vine_download(iframe_url, output_dir, merge=merge, info_only=info_only, **kwargs)
                return
            else:
                iframe_html = get_content(iframe_url)
                real_url = r1(r'<source src="([^"]*)"', iframe_html)

    title = unescape_html(r1(r'<meta property="og:title" content="([^"]*)" />', html) or
        r1(r'<meta property="og:description" content="([^"]*)" />', html) or
        r1(r'<title>([^<\n]*)', html) or url.split("/")[4]).replace('\n', '')

    # this is better
    vcode = r1(r'tumblr_(\w+)', real_url)
    real_url = 'https://vt.media.tumblr.com/tumblr_%s.mp4' % vcode

    type, ext, size = url_info(real_url, faker=True)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge=merge)

site_info = "Tumblr.com"
download = tumblr_download
download_playlist = playlist_not_supported('tumblr')
