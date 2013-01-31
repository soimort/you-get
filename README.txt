You-Get
=======

`You-Get <https://github.com/soimort/you-get>`_ is a video downloader runs on Python 3. It aims at easing the download of videos on `YouTube <http://www.youtube.com>`_, `Youku <http://www.youku.com>`_/`Tudou <http://www.tudou.com>`_ (biggest online video providers in China), etc., in one script.

See the project homepage http://www.soimort.org/you-get for further documentation.

Fork me on GitHub: https://github.com/soimort/you-get

Features
--------

Supported Sites (As of Now)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* YouTube http://www.youtube.com
* Vimeo http://vimeo.com
* Dailymotion http://dailymotion.com
* Facebook http://facebook.com
* Google+ http://plus.google.com
* Tumblr http://www.tumblr.com
* SoundCloud http://soundcloud.com
* Mixcloud http://www.mixcloud.com
* Youku (优酷) http://www.youku.com
* Tudou (土豆) http://www.tudou.com
* YinYueTai (音悦台) http://www.yinyuetai.com
* AcFun http://www.acfun.tv
* bilibili http://www.bilibili.tv
* CNTV (中国网络电视台) http://www.cntv.cn
* ifeng (凤凰视频) http://v.ifeng.com
* iQIYI (爱奇艺) http://www.iqiyi.com
* Joy.cn (激动网) http://www.joy.cn
* Ku6 (酷6网) http://www.ku6.com
* NetEase (网易视频) http://v.163.com
* PPTV http://www.pptv.com
* QQ (腾讯视频) http://v.qq.com
* Sina (新浪视频) http://video.sina.com.cn
* Sohu (搜狐视频) http://tv.sohu.com
* 56 (56网) http://www.56.com
* Xiami (虾米) http://www.xiami.com

Dependencies
------------

* `Python 3 <http://www.python.org/download/releases/>`_
* (Optional) `FFmpeg <http://ffmpeg.org>`_
    * Used for converting and joining video files.

Installation
------------

#) Install via `Pip <http://www.pip-installer.org/>`_::

    $ pip install you-get
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install via `EasyInstall <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install you-get
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install from Git::

    $ git clone git://github.com/soimort/you-get.git
    
   Use the raw script without installation::
    
    $ cd you-get/
    $ ./you-get -V
    
   To install the package into the system path, execute::
    
    $ make install
    
   Or (on Windows)::
    
    > setup.py install
    
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
    
   Or (on Windows)::
    
    > setup.py install
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install from `AUR (Arch User Repository) <http://aur.archlinux.org/>`_:

    Click `here <https://aur.archlinux.org/packages.php?ID=62576>`_.

Examples (For End-Users)
------------------------

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

Examples (For Developers)
-------------------------

In Python 3 (interactive)::

    >>> import you_get
    
    >>> you_get.__version__
    '0.2'
    
    >>> you_get.youtube_download("http://www.youtube.com/watch?v=8bQlxQJEzLk", info_only = True)
    Video Site: YouTube.com
    Title:      If you're good at something, never do it for free!
    Type:       WebM video (video/webm)
    Size:       0.13 MB (133176 Bytes)
    
    >>> you_get.any_download("http://www.youtube.com/watch?v=sGwy8DsUJ4M") 
    Video Site: YouTube.com
    Title:      Mort from Madagascar LIKES
    Type:       WebM video (video/webm)
    Size:       1.78 MB (1867072 Bytes)
    
    Downloading Mort from Madagascar LIKES.webm ...
    100.0% (  1.8/1.8  MB) [========================================] 1/1

API Reference
-------------

See source code.

License
-------

You-Get is licensed under the `MIT license <https://raw.github.com/soimort/you-get/master/LICENSE.txt>`_.
