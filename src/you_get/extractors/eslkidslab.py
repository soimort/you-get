from ..common import (
    get_content, re, download_urls, playlist_not_supported, print_info,
    url_info, parse, log
)


def get_play_source(url):
    source, play_source = None, None
    base_url = '/'.join(url.split('/')[:-1])
    html = get_content(url)
    if '_playListXML_Path' in html:
        play_path = re.search('_playListXML_Path=([^<>;"]+)', html).group(1)
        play_path_url = '{}/{}'.format(base_url, play_path)
        data = get_content(play_path_url)
        source = re.search('<source>(.+?)</source>', data).group(1)
    elif 'videoUrl' in html:
        source = re.search('videoUrl=([^&<>"]+)', html).group(1)

    if source:
        source = parse.quote(source)
        play_source = '{}/{}'.format(base_url, source)

    return play_source


def eslkidslab_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    url = parse.quote(url, safe=':/%')
    play_source = get_play_source(url)
    if not play_source:
        log.w('can not get video file, skip ...')
        return

    title = play_source.split('/')[-1].split('.')[0]
    title = parse.unquote(title)
    _, ext, size = url_info(play_source)
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([play_source], title, ext, size, output_dir, merge=merge)


site_info = 'eslkidslab.com'
download = eslkidslab_download
download_playlist = playlist_not_supported('eslkidslab')
