#!/usr/bin/env python

__all__ = ['ted_download']

from ..common import *
import json, os, inspect, logging, time
from pprint import pprint
#sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]
currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(os.path.dirname(currentDir))
se_parentDir = os.path.dirname(parentDir)
sys.path.append(parentDir)
sys.path.append(se_parentDir)
#print currentDir
#print parentDir
#print se_parentDir
# print sys.path

from you_get.common import *

TED_D_DINFO = False
TED_D_DSUB = False
TED_D_DFINFO = False

TED_TALKS_URL_PAT = "http://www.ted.com/talks/%s"
FOUND = False

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handle = logging.StreamHandler(sys.stdout)
log_handle.setFormatter(logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s'))
logger.addHandler(log_handle)

fake_headers_here = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Connection': 'keep-alive',
    'Cookie':'',
    }

def ted_download(url, output_dir='.', merge=True, info_only=False):
    html = get_html(url)
    metadata = json.loads(match1(html, r'({"talks"(.*)})\)'))
    title = metadata['talks'][0]['title']
    nativeDownloads = metadata['talks'][0]['nativeDownloads']
    for quality in ['high', 'medium', 'low']:
        if quality in nativeDownloads:
            url = nativeDownloads[quality]
            type, ext, size = url_info(url)
            print_info(site_info, title, type, size)
            if not info_only:
                download_urls([url], title, ext, size, output_dir, merge=merge)
            break

# For ted_download_by_id
re_url = re.compile('"nativeDownloads":.*"high":"(.+)\?.+},"sub')
re_slug = re.compile('"slug":"(.*?)"')
#re_vid = re.compile('http://.+\/(.*\.mp4)')
re_name = re.compile('"external":.*?,"name":"(.*?)","title":')
# Inner video ID
re_in_id = re.compile('http://www.ted.com/talks/(.*?)')

def ted_download_by_id(id, title, output_dir = '.', stream_type = None, merge = True, info_only = False, urls_only = False):
    # ret: urls,size,ext,headers = callMap[videoType](videoId,"title", urls_only = True)

    try:
        url = TED_TALKS_URL_PAT % id
        vpage = get_html(url)
    except:
        logger.info("###ted_download_by_id: TED id home can not be accessed")
        return [url], 0, 'mp4', {}

    logger.info("###ted_download_by_id")
    logger.info("page url is" + url)

    #print "page content is"
    # print vpage

    v_url = re.findall(re_url, vpage)[0]
    v_title = re.findall(re_name, vpage)[0]
    size = urls_size([v_url], True, None)
    #size is not used
    # size = -1
    urls = [v_url]

    logger.info("###ted_download_by_id")
    #logger.info("name + v_url + size \n" )
    #print "%r, %r, %r" % (v_title, v_url, size)
    logger.info("name: " + str(v_title) + " url:" + str(v_url) + " size: " + str(size))

    # print "ret is",(urls, size, 'mp4', 'fake_headers')

    return urls, size, 'mp4', {}


def ted_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False, urls_only = False):

    logger.info("###ted_download")
    logger.info("page url is " + url)

    vpage = get_html(url)
    v_title = re.findall(re_name, vpage)[0]
    v_url = re.findall(re_url, vpage)[0]

    type, ext, size = url_info(v_url)
    print_info(site_info, v_title, type, size)

    logger.info("v_title is " + str(v_title) + "type is " + str(type) + "size is " + str(size) )

    if not info_only:
        download_urls([v_url], v_title, ext, size, output_dir, merge = merge)


def get_videoId(url):
    v_in_id = re.findall(re_in_id, url)[0]
    return v_in_id


def srt_time(tst):
    """Format Time from TED Subtitles format to SRT time Format."""
    secs, mins, hours = ((tst / 1000) % 60), (tst / 60000), (tst / 3600000)
    right_srt_time = ("{0:02d}:{1:02d}:{2:02d},{3:3.0f}".
                      format(int(hours), int(mins), int(secs),
                             divmod(secs, 1)[1] * 1000))
    return right_srt_time


def srt_sec_time(tst):
    """Format Time from TED Subtitles format to SRT time Format."""
    secs = tst / 1000
    return secs


# regex expressions to search into the webpage
re_dm_intro = re.compile('"introDuration":(\d+\.?\d+),')
re_dm_id = re.compile('"id":(\d+),')
re_dm_url = re.compile('"nativeDownloads":.*"high":"(.+)\?.+},"sub')
re_dm_vid = re.compile('http://.+\/(.*\.mp4)')

def ted_get_danmu(video_id):
    """
    Get Danmu for the unique video_id
    """
    logger.info("###ted_get_danmu")

    url = TED_TALKS_URL_PAT % video_id
    logger.info("page url is " + url)

    try:
        vpage = get_html(url)
    except:
        logger.info("###ted_get_danmu:request faild, ret null danmu list")
        return []

    ret_list = []

    tt_intro = ((float(re_dm_intro.findall(vpage)[0]) + 1) * 1000)
    tt_id = int(re_dm_id.findall(vpage)[0])
    tt_url = re_dm_url.findall(vpage)[0]
    tt_v_fname = re_dm_vid.findall(tt_url)[0]

    #logger.info("###tt_intro is " + str(tt_intro))
    subs = get_subs(tt_id, tt_intro, tt_v_fname)

    # we only process english caption currrently
    # 0(eng) 0(item list)
    eng_sub = subs[0][0]

    for i in eng_sub:
        r_item = {}
        p_item = parse_item(i)

        r_item['text'] = p_item["content"]
        r_item['color'] = p_item["font_color"]
        r_item['fontSize'] = p_item["font_size"]
        r_item['direct'] = p_item["mode"]
        r_item['startTime'] = p_item["time"]
        r_item['uuid'] = p_item["uuid"]
        r_item['publishTime'] = p_item["pub_time"]

        ret_list.append(r_item)
        #logger.info("###parsed sub item")
        #pprint(r_item)

    logger.info("###ted_get_danmu:parsed sub item list info:" + " len: " + str(len(ret_list)))

    if TED_D_DINFO:
        logger.info("###ted_get_danmu:last two items" + " ret_list len " + str(len(ret_list) ) )
        if len(ret_list) > 0:
            pprint(ret_list[-1])
        if len(ret_list) > 1:
            pprint(ret_list[-2])
        pass

    if TED_D_DFINFO:
        logger.info("###ted_get_danmu:full ret list" )
        logger.info(str(ret_list))

    return ret_list


def parse_item(item):
    """
    Return a tuple for a+ danmu element
    """
    s_time = float(item["start"])

    # Mode is the direct opt
    # mode 1~3: scrolling
    # mode 4: bottom
    # mode 5: top
    # mode 6: reverse?
    # mode 7: position
    # mode 8: advanced
    mode = 4
    assert 1 <= mode <= 8

    # pool 0: normal
    # pool 1: srt
    # pool 2: special?
    #pool = int(pool)
    pool = 0
    assert 0 <= pool <= 2

    font_size = 25
    font_color = 16777215
    pub_time = str(int(time.time() * 1000000 ))[-10:]

    return {"time":s_time, "font_color":font_color, "mode":mode, "font_size":font_size,
            "uuid":"s_defuuid_z9", "pub_time":pub_time, "content":item["content"]}


def get_subs(tt_id, tt_intro, tt_video_fname):
    """
    Get the sutitles, currently for english
    """

    subs = ["{0}.{1}.srt".format(tt_video_fname[:-4], lang) for lang in ('eng', 'chi')]
    ret_subs = []

    for sub in subs:
        #logger.info("###get_subs:pls input to continue s sub getting:")
        #raw_input()

        subtitle = get_single_sub(tt_id, tt_intro, sub)
        if subtitle:
            ret_subs.append(subtitle)
            #logger.info("###get_subs:Subtitle '{0}' downloaded.".format(sub) )

    if TED_D_DSUB:
        # raw_input()
        logger.info("\n")
        for idx, sub in enumerate(subs):

            with open(sub, 'w') as srt_file:
                for item in ret_subs[idx][0]:
                    srt_file.write(str(item))

                srt_file.write("\n#############\n")
                srt_file.write("\nSRT formated data\n")
                srt_file.write(ret_subs[idx][1])

            logger.info("###get_subs:Debug:Subtitle '{0}' downloaded.".format(sub))

    return ret_subs


def get_single_sub(tt_id, tt_intro, sub):
    """
    Get TED Subtitle in JSON format & convert it to SRT Subtitle.
    """

    srt_content = ''
    srt_items = []
    tt_url = 'http://www.ted.com/talks'
    sub_url = '{0}/subtitles/id/{1}/lang/{2}'.format(tt_url, tt_id, sub[-7:-4])

    # Get JSON sub
    json_file = request.urlopen(sub_url).readlines()
    logger.info("###get_single_sub: sub url is " + sub_url)

    if json_file:
        try:
            json_object = json.loads(json_file[0].decode('utf-8'))
            logger.info("###get_single_sub: json load orig data")
            #logger.info(json_object)
            if 'captions' in json_object:
                caption_idx = 1
                if not json_object['captions']:
                    logger.info("Subtitle '{0}' not available.".format(sub))
                for caption in json_object['captions']:
                    start = tt_intro + caption['startTime']
                    end = start + caption['duration']
                    idx_line = '{0}'.format(caption_idx)
                    time_line = '{0} --> {1}'.format(srt_time(start),
                                                     srt_time(end))
                    text_line = '{0}'.format(caption['content'].encode("utf-8"))

                    # Append the srt items and content parellelly
                    srt_items.append({"index":caption_idx, "start":srt_sec_time(start),
                                      "duration":srt_sec_time(caption['duration']), "content":text_line})
                    srt_content += '\n'.join([idx_line, time_line, text_line, '\n'])
                    caption_idx += 1

            elif 'status' in json_object:
                logger.info("This is an error message returned by TED:{0}{0} - "
                      "{1}{0}{0}Probably because the subtitle '{2}' is not "
                      "available.{0}".format(os.linesep, json_object['status']['message'], sub))

        except ValueError:
            logger.info("Subtitle '{0}' it's a malformed json file.".format(sub))

    return (srt_items, srt_content)


def options():
    """Defines the command line arguments and options for the script."""

    desc = "Downloads the subtitles and the video (optional) for a TED Talk."
    usage = "Beautifull TED"
    parser = optparse.OptionParser(usage=usage, version="%prog " + __version__,
                                   description=desc)

    parser.add_option("-s", "--only_subs", action='store_true',
                      dest="no_video",
                      help="download only the subs, not the video ",
                      default=False)
    return parser


def check_exec_posix(prog):
    """
    Check if the program is installed in a *NIX platform.
    """
    return True


def main():
    """main section"""
    pass


# module info
get_Danmu = ted_get_danmu


site_info = "TED.com"
download = ted_download
download_playlist = playlist_not_supported('ted')
