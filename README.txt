You-Get
=======

.. image:: https://api.travis-ci.org/soimort/you-get.png

.. image:: https://badge.fury.io/py/you-get.png

`You-Get <https://github.com/soimort/you-get>`_ is a video downloader runs on Python 3. It aims at easing the download of videos on `YouTube <http://www.youtube.com>`_, `Youku <http://www.youku.com>`_/`Tudou <http://www.tudou.com>`_ (biggest online video providers in China), `Niconico <http://www.nicovideo.jp>`_, etc., in one script.

See the project homepage http://www.soimort.org/you-get for further documentation.

Fork me on GitHub: https://github.com/soimort/you-get

Features
--------

Supported Sites (As of Now)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* YouTube http://www.youtube.com
* Vimeo http://vimeo.com
* Coursera https://www.coursera.org
* Blip http://blip.tv
* Dailymotion http://dailymotion.com
* eHow http://www.ehow.com
* Facebook http://facebook.com
* Google+ http://plus.google.com
* Google Drive http://docs.google.com
* Khan Academy http://www.khanacademy.org
* TED http://www.ted.com
* Tumblr http://www.tumblr.com
* Vine http://vine.co
* Instagram http://instagram.com
* SoundCloud http://soundcloud.com
* Mixcloud http://www.mixcloud.com
* Freesound http://www.freesound.org
* JPopsuki http://jpopsuki.tv
* VID48 http://vid48.com
* Niconico (ニコニコ動画) http://www.nicovideo.jp
* Youku (优酷) http://www.youku.com
* Tudou (土豆) http://www.tudou.com
* YinYueTai (音悦台) http://www.yinyuetai.com
* AcFun http://www.acfun.tv
* bilibili http://www.bilibili.tv
* CNTV (中国网络电视台) http://www.cntv.cn
* Douban (豆瓣) http://douban.com
* ifeng (凤凰视频) http://v.ifeng.com
* iQIYI (爱奇艺) http://www.iqiyi.com
* Joy.cn (激动网) http://www.joy.cn
* Ku6 (酷6网) http://www.ku6.com
* LeTV (乐视网) http://www.letv.com
* MioMio http://www.miomio.tv
* NetEase (网易视频) http://v.163.com
* PPTV http://www.pptv.com
* QQ (腾讯视频) http://v.qq.com
* Sina (新浪视频) http://video.sina.com.cn
* Sohu (搜狐视频) http://tv.sohu.com
* 56 (56网) http://www.56.com
* Xiami (虾米) http://www.xiami.com
* 5sing http://www.5sing.com
* Baidu Music (百度音乐) http://music.baidu.com
* Baidu Wangpan (百度网盘) http://pan.baidu.com
* SongTaste http://www.songtaste.com
* Alive.in.th http://alive.in.th

Dependencies
------------

* `Python 3 <http://www.python.org/download/releases/>`_
* (Optional) `FFmpeg <http://ffmpeg.org>`_
    * Used for converting and joining video files.

Installation
------------

#) Install via Pip::

    $ [sudo] pip install you-get
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install from Git::

    $ git clone git://github.com/soimort/you-get.git
    
   Use the raw script without installation::
    
    $ cd you-get/
    $ ./you-get -V
    
   To install the package into the system path, execute::
    
    $ make install
    
   Check if the installation was successful::
    
    $ you-get -V

#) Direct download::
    
    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip
    
   Use the raw script without installation::
    
    $ cd soimort-you-get-*/
    $ ./you-get -V
    
   To install the package into the system path, execute::
    
    $ make install
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install from your distro's repo:

* `AUR (Arch) <https://aur.archlinux.org/packages/?O=0&K=you-get>`_

* `Overlay (Gentoo) <http://gpo.zugaina.org/net-misc/you-get>`_

Upgrading
---------

Using Pip::

    $ [sudo] pip install --upgrade you-get

Examples
--------

Display the information of the video without downloading::

    $ you-get -i http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download the video::

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download multiple videos::

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M http://www.youtube.com/watch?v=8bQlxQJEzLk

By default, program will skip any video that already exists in the local directory when downloading. If a temporary file (ends with a ".download" filename extension) is found, program will resume the download from last session.

To enforce re-downloading of videos, use '-f' option (this will overwrite any existing video or temporary file, rather than skipping or resuming them)::

    $ you-get -f http://www.youtube.com/watch?v=sGwy8DsUJ4M

Set the output directory for downloaded files::

    $ you-get -o ~/Downloads http://www.youtube.com/watch?v=sGwy8DsUJ4M

Use a specific HTTP proxy for downloading::

    $ you-get -x 127.0.0.1:8087 http://www.youtube.com/watch?v=sGwy8DsUJ4M

By default, Python will apply the system proxy settings (i.e. environment variable $http_proxy). To cancel the use of proxy, use '--no-proxy' option::

    $ you-get --no-proxy http://www.youtube.com/watch?v=sGwy8DsUJ4M

Command-Line Options
--------------------

For a complete list of all available options, see::

    $ you-get --help
    Usage: you-get [OPTION]... [URL]...
    
    Startup options:
        -V | --version                           Display the version and exit.
        -h | --help                              Print this help and exit.
    
    Download options (use with URLs):
        -f | --force                             Force overwriting existed files.
        -i | --info                              Display the information of videos without downloading.
        -u | --url                               Display the real URLs of videos without downloading.
        -n | --no-merge                          Don't merge video parts.
        -o | --output-dir <PATH>                 Set the output directory for downloaded videos.
        -p | --player <PLAYER [options]>         Directly play the video with PLAYER like vlc/smplayer.
        -x | --http-proxy <HOST:PORT>            Use specific HTTP proxy for downloading.
             --no-proxy                          Don't use any proxy. (ignore $http_proxy)
        -S | --sogou                             Use a Sogou proxy server for downloading.
             --sogou-proxy <HOST:PORT>           Run a standalone Sogou proxy server.
             --debug                             Show traceback on KeyboardInterrupt.

License
-------

You-Get is licensed under the `MIT license <https://raw.github.com/soimort/you-get/master/LICENSE.txt>`_.

Contributing
------------

Please see `CONTRIBUTING.md <https://github.com/soimort/you-get/blob/master/CONTRIBUTING.md>`_.
