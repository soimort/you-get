#!/usr/bin/env python

__all__ = ['coursera_download']

from ..common import *

def coursera_login(user, password, csrf_token):
    url = 'https://www.coursera.org/maestro/api/user/login'
    my_headers = {
        'Cookie': ('csrftoken=%s' % csrf_token),
        'Referer': 'https://www.coursera.org',
        'X-CSRFToken': csrf_token,
    }
    
    values = {
        'email_address': user,
        'password': password,
    }
    form_data = parse.urlencode(values).encode('utf-8')
    
    response = request.urlopen(request.Request(url, headers = my_headers, data = form_data))
    
    return response.headers

def coursera_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    course_code = r1(r'coursera.org/([^/]+)', url)
    url = "http://class.coursera.org/%s/lecture/index" % course_code
    
    request.install_opener(request.build_opener(request.HTTPCookieProcessor()))
    
    import http.client
    conn = http.client.HTTPConnection('class.coursera.org')
    conn.request('GET', "/%s/lecture/index" % course_code)
    response = conn.getresponse()
    
    csrf_token = r1(r'csrf_token=([^;]+);', response.headers['Set-Cookie'])
    
    import netrc, getpass
    info = netrc.netrc().authenticators('coursera.org')
    if info is None:
        user = input("User:     ")
        password = getpass.getpass("Password: ")
    else:
        user, password = info[0], info[2]
    print("Logging in...")
    
    coursera_login(user, password, csrf_token)
    
    request.urlopen("https://class.coursera.org/%s/auth/auth_redirector?type=login&subtype=normal" % course_code) # necessary!
    
    html = get_html(url)
    
    course_name = "%s (%s)" % (r1(r'course_strings_name = "([^"]+)"', html), course_code)
    output_dir = os.path.join(output_dir, course_name)
    
    materials = re.findall(r'<a target="_new" href="([^"]+)"', html)
    num_of_slides = len(re.findall(r'title="[Ss]lides', html))
    num_of_srts = len(re.findall(r'title="Subtitles \(srt\)"', html))
    num_of_texts = len(re.findall(r'title="Subtitles \(text\)"', html))
    num_of_mp4s = len(re.findall(r'title="Video \(MP4\)"', html))
    num_of_others = len(materials) - num_of_slides - num_of_srts - num_of_texts - num_of_mp4s
    
    print("MOOC Site:               ", site_info)
    print("Course Name:             ", course_name)
    print("Num of Videos (MP4):     ", num_of_mp4s)
    print("Num of Subtitles (srt):  ", num_of_srts)
    print("Num of Subtitles (text): ", num_of_texts)
    print("Num of Slides:           ", num_of_slides)
    print("Num of other resources:  ", num_of_others)
    print()
    
    if info_only:
        return
    
    # Process downloading
    
    names = re.findall(r'<div class="hidden">([^<]+)</div>', html)
    assert len(names) == len(materials)
    
    for i in range(len(materials)):
        title = names[i]
        resource_url = materials[i]
        ext = r1(r'format=(.+)', resource_url) or r1(r'\.(\w\w\w\w|\w\w\w|\w\w|\w)$', resource_url) or r1(r'download.(mp4)', resource_url)
        _, _, size = url_info(resource_url)
        
        try:
            if ext == 'mp4':
                download_urls([resource_url], title, ext, size, output_dir, merge = merge)
            else:
                download_url_chunked(resource_url, title, ext, size, output_dir, merge = merge)
        except Exception as err:
            print('Skipping %s: %s\n' % (resource_url, err))
            continue
    
    return

def download_url_chunked(url, title, ext, size, output_dir = '.', refer = None, merge = True, faker = False):
    if dry_run:
        print('Real URL:\n', [url], '\n')
        return
    
    title = escape_file_path(title)
    if ext:
        filename = '%s.%s' % (title, ext)
    else:
        filename = title
    filepath = os.path.join(output_dir, filename)
    
    if not force and os.path.exists(filepath):
        print('Skipping %s: file already exists' % tr(filepath))
        print()
        return
    
    bar = DummyProgressBar()
    print('Downloading %s ...' % tr(filename))
    url_save_chunked(url, filepath, bar, refer = refer, faker = faker)
    bar.done()
    
    print()
    return

site_info = "Coursera"
download = coursera_download
download_playlist = playlist_not_supported('coursera')
