# You-Get

[![Build Status](https://api.travis-ci.org/soimort/you-get.png)](https://travis-ci.org/soimort/you-get) [![PyPI version](https://badge.fury.io/py/you-get.png)](http://badge.fury.io/py/you-get) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/soimort/you-get?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[You-Get](http://www.soimort.org/you-get) is a video downloader for [YouTube](http://www.youtube.com), [Youku](http://www.youku.com), [niconico](http://www.nicovideo.jp) and a few other sites.

`you-get` is a command-line program, written completely in Python 3. Its prospective users are those who prefer CLI over GUI. With `you-get`, downloading a video is just one command away:

    $ you-get http://youtu.be/sGwy8DsUJ4M

Fork me on GitHub: <https://github.com/soimort/you-get>

## Features

### Supported Sites

* Dailymotion <http://dailymotion.com>
* Freesound <http://www.freesound.org>
* Google+ <http://plus.google.com>
* Instagram <http://instagram.com>
* JPopsuki <http://jpopsuki.tv>
* Magisto <http://www.magisto.com>
* Mixcloud <http://www.mixcloud.com>
* Niconico (ニコニコ動画) <http://www.nicovideo.jp>
* Vimeo <http://vimeo.com>
* Vine <http://vine.co>
* Twitter <http://twitter.com>
* Youku (优酷) <http://www.youku.com>
* YouTube <http://www.youtube.com>
* AcFun <http://www.acfun.tv>
* Alive.in.th <http://alive.in.th>
* Baidu Music (百度音乐) <http://music.baidu.com>
* Baidu Wangpan (百度网盘) <http://pan.baidu.com>
* Baomihua (爆米花) <http://video.baomihua.com>
* bilibili <http://www.bilibili.com>
* Blip <http://blip.tv>
* Catfun (喵星球) <http://www.catfun.tv>
* CBS <http://www.cbs.com>
* CNTV (中国网络电视台) <http://www.cntv.cn>
* Coursera <https://www.coursera.org>
* Dongting (天天动听) <http://www.dongting.com>
* Douban (豆瓣) <http://douban.com>
* DouyuTV (斗鱼) <http://www.douyutv.com>
* eHow <http://www.ehow.com>
* Facebook <http://facebook.com>
* Google Drive <http://docs.google.com>
* ifeng (凤凰视频) <http://v.ifeng.com>
* iQIYI (爱奇艺) <http://www.iqiyi.com>
* Joy.cn (激动网) <http://www.joy.cn>
* Khan Academy <http://www.khanacademy.org>
* Ku6 (酷6网) <http://www.ku6.com>
* Kugou (酷狗音乐) <http://www.kugou.com>
* Kuwo (酷我音乐) <http://www.kuwo.cn>
* LeTV (乐视网) <http://www.letv.com>
* Lizhi.fm (荔枝FM) <http://www.lizhi.fm>
* MioMio <http://www.miomio.tv>
* MTV 81 <http://www.mtv81.com>
* NetEase (网易视频) <http://v.163.com>
* NetEase Music (网易云音乐) <http://music.163.com>
* PPTV <http://www.pptv.com>
* QQ (腾讯视频) <http://v.qq.com>
* Sina (新浪视频) <http://video.sina.com.cn>
* Sohu (搜狐视频) <http://tv.sohu.com>
* SongTaste <http://www.songtaste.com>
* SoundCloud <http://soundcloud.com>
* TED <http://www.ted.com>
* Tudou (土豆) <http://www.tudou.com>
* Tumblr <http://www.tumblr.com>
* VID48 <http://vid48.com>
* VideoBam <http://videobam.com>
* VK <http://vk.com>
* 56 (56网) <http://www.56.com>
* Xiami (虾米) <http://www.xiami.com>
* YinYueTai (音悦台) <http://www.yinyuetai.com>
* Zhanqi (战旗TV) <http://www.zhanqi.tv/lives>

## Prerequisites

### Python 3

`you-get` is known to work with:

* Python 3.2
* Python 3.3
* Python 3.4
* PyPy3

`you-get` does not (and will never) work with Python 2.x.

### Dependencies (Optional but Recommended)

* [FFmpeg](http://ffmpeg.org) or [Libav](http://libav.org/)
    * For video and audio processing.
* [RTMPDump](http://rtmpdump.mplayerhq.hu/)
    * For RTMP stream processing.

## Installation

You don't have to learn the Python programming language to use this tool. However, you need to make sure that Python 3 (with pip) is installed on your system.

On Linux and BSD, installation made easy with your package manager:

* Find and install packages: `python3` and `python3-pip` (if your distro did not make Python 3 the default, e.g., Debian)
* Or packages: `python` and `python-pip` (if your distro made Python 3 the default, e.g., Arch)

On other systems (which tend to have quite evil user experience), please read the documentation and ask Google for help:

* <https://www.python.org/downloads/>
* <https://pip.pypa.io/en/latest/installing.html>

### 1. Using Pip (Standard Method)

    $ [sudo] pip3 install you-get

Check if the installation is successful:

    $ you-get -V

### 2. Downloading from PyPI

You can also download the Python wheel for each release from [PyPI](https://pypi.python.org/pypi/you-get).

If you choose to download the wheel from a PyPI mirror or elsewhere, remember to verify the signature of the package. For example:

    $ gpg --verify you_get-0.3.30-py3-none-any.whl.asc you_get-0.3.30-py3-none-any.whl

### 3. Downloading from GitHub

Download it [here](https://github.com/soimort/you-get/zipball/master) or:

    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip

Use the raw script without installation:

    $ cd soimort-you-get-*/
    $ ./you-get -V

To install the package into the system path, execute:

    $ [sudo] make install

Check if the installation is successful:

    $ you-get -V

### 4. Using Git (Recommended for Developers and Advanced Users)

    $ git clone git://github.com/soimort/you-get.git

Use the raw script without installation:

    $ cd you-get/
    $ ./you-get -V

To install the package into the system path, execute:

    $ [sudo] make install

Check if the installation is successful:

    $ you-get -V

## Upgrading

### 1. Using Pip

    $ [sudo] pip3 install --upgrade you-get

## Getting Started

Display the information of a video without downloading:

    $ you-get -i 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Download a video:

    $ you-get 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Download multiple videos:

    $ you-get 'http://www.youtube.com/watch?v=sGwy8DsUJ4M' 'http://www.youtube.com/watch?v=8bQlxQJEzLk'

By default, program will skip any video that already exists in the local directory when downloading. If a temporary file (ends with a `.download` extension in its file name) is found, program will resume the download from last session.

To enforce re-downloading of videos, use option `-f`: (this will overwrite any existing video or temporary file)

    $ you-get -f 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Set the output directory for downloaded files:

    $ you-get -o ~/Downloads 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Use a specific HTTP proxy for downloading:

    $ you-get -x 127.0.0.1:8087 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

By default, the system proxy setting (i.e. environment variable `http_proxy` on *nix) is applied. To disable any proxy, use option `--no-proxy`:

    $ you-get --no-proxy 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Watch a video in your media player of choice: (this is just a trick to let you get rid of annoying ads on the video site)

    $ you-get -p vlc 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

## FAQ

**Q**: Some videos on Youku are restricted to mainland China visitors. Is it possible to bypass this restriction and download those videos?

**A**: Thanks to [Unblock Youku](https://github.com/zhuzhuor/Unblock-Youku), it is now possible to access such videos from an oversea IP address. You can simply use `you-get` with option `-y proxy.uku.im:8888`.

**Q**: Will you release an executable version / Windows Installer package?

**A**: Yes, it's on my to-do list.

## Command-Line Options

For a complete list of available options, see:

```
$ you-get --help
Usage: you-get [OPTION]... [URL]...

Startup options:
    -V | --version                           Display the version and exit.
    -h | --help                              Print this help and exit.

Download options (use with URLs):
    -f | --force                             Force overwriting existed files.
    -i | --info                              Display the information of videos without downloading.
    -u | --url                               Display the real URLs of videos without downloading.
    -c | --cookies                           Load NetScape's cookies.txt file.
    -n | --no-merge                          Don't merge video parts.
    -F | --format <STREAM_ID>                Video format code.
    -o | --output-dir <PATH>                 Set the output directory for downloaded videos.
    -p | --player <PLAYER [options]>         Directly play the video with PLAYER like vlc/smplayer.
    -x | --http-proxy <HOST:PORT>            Use specific HTTP proxy for downloading.
    -y | --extractor-proxy <HOST:PORT>       Use specific HTTP proxy for extracting stream data.
         --no-proxy                          Don't use any proxy. (ignore $http_proxy)
         --debug                             Show traceback on KeyboardInterrupt.
```

## License

You-Get is licensed under the [MIT license](https://raw.github.com/soimort/you-get/master/LICENSE.txt).

## Reporting an Issue / Contributing

Please read [CONTRIBUTING.md](https://github.com/soimort/you-get/blob/master/CONTRIBUTING.md) first.
