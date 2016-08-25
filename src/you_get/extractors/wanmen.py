#!/usr/bin/env python

__all__ = ['wanmen_download', 'wanmen_download_by_course', 'wanmen_download_by_course_topic', 'wanmen_download_by_course_topic_part']

from ..common import *
from .bokecc import bokecc_download_by_id
from json import loads


##Helper functions
def _wanmen_get_json_api_content_by_courseID(courseID):
    """int->JSON
    
    Return a parsed JSON tree of WanMen's API."""

    return loads(get_content('http://api.wanmen.org/course/getCourseNested/{courseID}'.format(courseID = courseID)))

def _wanmen_get_title_by_json_topic_part(json_content, tIndex, pIndex):
    """JSON, int, int, int->str
    
    Get a proper title with courseid+topicID+partID."""

    return '_'.join([json_content[0]['name'],
                    json_content[0]['Topics'][tIndex]['name'],
                    json_content[0]['Topics'][tIndex]['Parts'][pIndex]['name']])


def _wanmen_get_boke_id_by_json_topic_part(json_content, tIndex, pIndex):
    """JSON, int, int, int->str
    
    Get one BokeCC video ID with courseid+topicID+partID."""

    return json_content[0]['Topics'][tIndex]['Parts'][pIndex]['ccVideoLink']


##Parsers
def wanmen_download_by_course(json_api_content, output_dir='.', merge=True, info_only=False, **kwargs):
    """int->None
    
    Download a WHOLE course.
    Reuse the API call to save time."""

    for tIndex in range(len(json_api_content[0]['Topics'])):
        for pIndex in range(len(json_api_content[0]['Topics'][tIndex]['Parts'])):
            wanmen_download_by_course_topic_part(json_api_content,
                                                 tIndex,
                                                 pIndex,
                                                 output_dir=output_dir,
                                                 merge=merge,
                                                 info_only=info_only,
                                                 **kwargs)


def wanmen_download_by_course_topic(json_api_content, tIndex, output_dir='.', merge=True, info_only=False, **kwargs):
    """int, int->None
    
    Download a TOPIC of a course.
    Reuse the API call to save time."""

    for pIndex in range(len(json_api_content[0]['Topics'][tIndex]['Parts'])):
        wanmen_download_by_course_topic_part(json_api_content,
                                             tIndex,
                                             pIndex, 
                                            output_dir=output_dir,
                                            merge=merge,
                                            info_only=info_only,
                                            **kwargs)

def wanmen_download_by_course_topic_part(json_api_content, tIndex, pIndex, output_dir='.', merge=True, info_only=False, **kwargs):
    """int, int, int->None
    
    Download ONE PART of the course."""

    html = json_api_content

    title = _wanmen_get_title_by_json_topic_part(html, 
                                                  tIndex, 
                                                  pIndex)

    bokeccID = _wanmen_get_boke_id_by_json_topic_part(html,
                                                      tIndex, 
                                                     pIndex)

    bokecc_download_by_id(vid = bokeccID, title = title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)


##Main entrance
def wanmen_download(url, output_dir='.', merge=True, info_only=False, **kwargs):

    if not 'wanmen.org' in url:
        log.wtf('You are at the wrong place dude. This is for WanMen University!')
        raise

    courseID = int(match1(url, r'course\/(\d+)'))
    assert courseID > 0  #without courseID we cannot do anything

    tIndex = int(match1(url, r'tIndex=(\d+)'))

    pIndex = int(match1(url, r'pIndex=(\d+)'))

    json_api_content = _wanmen_get_json_api_content_by_courseID(courseID)

    if pIndex:  #only download ONE single part
        assert tIndex >= 0
        wanmen_download_by_course_topic_part(json_api_content, tIndex, pIndex, 
                                            output_dir = output_dir, 
                                            merge = merge, 
                                            info_only = info_only)
    elif tIndex:  #download a topic
        wanmen_download_by_course_topic(json_api_content, tIndex, 
                                       output_dir = output_dir, 
                                       merge = merge, 
                                       info_only = info_only)
    else:  #download the whole course
        wanmen_download_by_course(json_api_content,
                                 output_dir = output_dir, 
                                 merge = merge, 
                                 info_only = info_only)


site_info = "WanMen University"
download = wanmen_download
download_playlist = wanmen_download_by_course