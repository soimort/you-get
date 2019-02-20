#!/usr/bin/env python

__all__ = ['zhihu_download', 'zhihu_download_playlist']

from ..common import *
import json


def zhihu_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    paths = url.split("/")
    # question or column
    if len(paths) < 3 and len(paths) < 6:
        raise TypeError("URL does not conform to specifications, Support column and question only."
                        "Example URL: https://zhuanlan.zhihu.com/p/51669862 or "
                        "https://www.zhihu.com/question/267782048/answer/490720324")

    if ("question" not in paths or "answer" not in paths) and "zhuanlan.zhihu.com" not in paths:
        raise TypeError("URL does not conform to specifications, Support column and question only."
                        "Example URL: https://zhuanlan.zhihu.com/p/51669862 or "
                        "https://www.zhihu.com/question/267782048/answer/490720324")

    html = get_html(url, faker=True)
    title = match1(html, r'data-react-helmet="true">(.*?)</title>')
    for index, video_id in enumerate(matchall(html, [r'<a class="video-box" href="\S+video/(\d+)"'])):
        try:
            video_info = json.loads(
                get_content(r"https://lens.zhihu.com/api/videos/{}".format(video_id), headers=fake_headers))
        except json.decoder.JSONDecodeError:
            log.w("Video id not found:{}".format(video_id))
            continue

        play_list = video_info["playlist"]
        # first High Definition
        # second Second Standard Definition
        # third ld. What is ld ?
        # finally continue
        data = play_list.get("hd", play_list.get("sd", play_list.get("ld", None)))
        if not data:
            log.w("Video id No play address:{}".format(video_id))
            continue
        print_info(site_info, title, data["format"], data["size"])
        if not info_only:
            ext = "_{}.{}".format(index, data["format"])
            if kwargs.get("zhihu_offset"):
                ext = "_{}".format(kwargs["zhihu_offset"]) + ext
            download_urls([data["play_url"]], title, ext, data["size"],
                          output_dir=output_dir, merge=merge, **kwargs)


def zhihu_download_playlist(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if "question" not in url or "answer" in url:  # question page
        raise TypeError("URL does not conform to specifications, Support question only."
                        " Example URL: https://www.zhihu.com/question/267782048")
    url = url.split("?")[0]
    if url[-1] == "/":
        question_id = url.split("/")[-2]
    else:
        question_id = url.split("/")[-1]
    videos_url = r"https://www.zhihu.com/api/v4/questions/{}/answers".format(question_id)
    try:
        questions = json.loads(get_content(videos_url))
    except json.decoder.JSONDecodeError:
        raise TypeError("Check whether the problem URL exists.Example URL: https://www.zhihu.com/question/267782048")

    count = 0
    while 1:
        for data in questions["data"]:
            kwargs["zhihu_offset"] = count
            zhihu_download("https://www.zhihu.com/question/{}/answer/{}".format(question_id, data["id"]),
                           output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
            count += 1
        if questions["paging"]["is_end"]:
            return
        questions = json.loads(get_content(questions["paging"]["next"], headers=fake_headers))


site_info = "zhihu.com"
download = zhihu_download
download_playlist = zhihu_download_playlist
