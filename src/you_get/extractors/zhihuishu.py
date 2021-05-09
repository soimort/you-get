from ..common import *

import time
import json


class zhihuishu(object):
    def __init__(self):
        referer = {
            'Referer': 'https://studyh5.zhihuishu.com/'
        }
        fake_headers.update(referer)

    def parse_recruit_and_video(self, url):
        if not ('recruitAndCourseId' in url):
            raise KeyError('Wrong URL or We can not parse the format'
                           'Please make sure URL like: https://studyh5.zhihuishu.com/videoStudy.html#/studyVideo?recruitAndCourseId=4f5d595c46524258454a5859504c5a45')
        return url.split('?')[-1].split('=')[-1]

    def get_uuid(self):
        uinx_time = int(time.time())
        url = 'https://studyservice.zhihuishu.com/login/getLoginUserInfo?dateFormate=%s' % uinx_time
        data = json.loads(get_content(url, headers=fake_headers))
        if data['code'] == 403:
            raise KeyError('Can not request uuid Please check you cookies')
        return data['data']['uuid']

    def get_video_ids(self, recruit_and_course_id, uuid):
        url = 'https://studyservice.zhihuishu.com/learning/videolist'
        post_data = {
            'uuid': uuid,
            'recruitAndCourseId': recruit_and_course_id,
            'dateFormate': '%s' % int(time.time())
        }
        data = post_content(url, headers=fake_headers, post_data=post_data)
        data = json.loads(data)['data']
        video_chapter_dtos = data['videoChapterDtos']
        videos_name_and_id = {}
        for video_chapter_dto in video_chapter_dtos:
            video_lessons = video_chapter_dto['videoLessons']
            for video_lesson in video_lessons:
                # 小节中的小节
                if 'videoSmallLessons' in video_lesson.keys():
                    for video_small_lesson in video_lesson['videoSmallLessons']:
                        videos_name_and_id[video_small_lesson['name']
                                           ] = video_small_lesson['videoId']
                else:
                    videos_name_and_id[video_lesson['name']
                                       ] = video_lesson['videoId']
        return videos_name_and_id

    def get_video_urls(self, videos_name_and_id):
        url = 'https://newbase.zhihuishu.com/video/initVideo?jsonpCallBack=result&videoID=%s&_=%s'
        videos_name_and_url = {}
        for video_name in videos_name_and_id:
            data = json.loads(get_content(
                url % (videos_name_and_id[video_name], int(time.time())), headers=fake_headers)[7:-1])
            video_types = data['result']['lines']
            for video_type in video_types:
                if video_type['lineDefault']:
                    videos_name_and_url[video_name] = video_type['lineUrl']
        return videos_name_and_url

    def download(self, url, **kwargs):
        raise Exception(
            'Support a list of courses only, Which URL like https://studyh5.zhihuishu.com/videoStudy.html#/studyVideo?recruitAndCourseId=4f5d595c46524258454a5859504c5a45'
            'Please use -l , if URL is right'
        )

    def download_playlist(self, url, **kwargs):
        # 从url拿到recruitAndCourseId
        recruit_and_course_id = self.parse_recruit_and_video(url)
        # 通过cookie请求用户信息
        if not cookies:
            raise KeyError(
                'You need to set cookies to download the course video'
                'Example: you-get -c Cookies.txt URL')
        uuid = self.get_uuid()
        # 请求video list
        # 解析返回的video ID
        videos_name_and_id = self.get_video_ids(recruit_and_course_id, uuid)
        # 通过video ID 请求视频地址
        videos_name_and_url = self.get_video_urls(videos_name_and_id)
        # 循环下载
        for index, video_name in enumerate(videos_name_and_url):
            url = videos_name_and_url[video_name]
            ext = url.split('/')[-1].split('.')[-1]
            file_name = str(index)+'-'+video_name
            download_urls([url], file_name, ext, headers=fake_headers,
                          total_size=None, **kwargs)


site = zhihuishu()
download = site.download
download_playlist = site.download_playlist
