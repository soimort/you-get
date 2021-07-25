import traceback
import sys
from you_get import common as you_get
import io
import os

url = "https://www.bilibili.com/video/BV1GV411p7P9"
path = os.path.dirname(os.path.realpath(__file__))

def getJson(url):
    try:
        __console__ = sys.stdout
        f = io.StringIO()
        sys.stdout = f
        sys.argv = ['you-get', url, '--json']
        you_get.main()
        text = f.getvalue()
        sys.stdout = __console__
        print(text)
    except:
        traceback.print_exc()


def getDefaultDownloadInfo(url):
    try:
        __console__ = sys.stdout
        f = io.StringIO()
        sys.stdout = f
        sys.argv = ['you-get', url, '-u']
        you_get.main()
        text = f.getvalue()
        sys.stdout = __console__
        print(text)
    except:
        traceback.print_exc()


def download(url, path):
    try:
        sys.argv = ['you-get', url, '-o', path, '--no-caption', '--debug']
        you_get.main()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    # only use one sentence, they all ok （使用如下的单条语句，都是可以正常打印的， 并且可以下载视频）
    # both are cant download video with combine （但是将语句组合使用，打印出的结果就有问题了， 并且无法下载视频）

    # use these lines, print double json text （使用如下语句，将会打印出两次 json 解析数据）
    getDefaultDownloadInfo(url)
    getJson(url)
    download(url, path)

    # or use these lines, print triple json text （使用如下语句，仅仅改变排序，将会打印出三次 json 解析数据）
    # getJson(url)
    # getDefaultDownloadInfo(url)
    # download(url, "save path")
