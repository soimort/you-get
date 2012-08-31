You-Get
=======

`You-Get <https://github.com/soimort/you-get>`_ is a video downloader runs on Python 3. It aims at easing the download of videos on `YouTube <http://www.youtube.com>`_, `Youku <http://www.youku.com>`_/`Tudou <http://www.tudou.com>`_ (biggest online video providers in China), etc., in one tool.

See the project homepage http://www.soimort.org/you-get for further documentation.

Fork me on GitHub: https://github.com/soimort/you-get

Features
--------

Supported Sites (UPDATING!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* YouTube http://www.youtube.com
* Youku http://www.youku.com
* Tudou http://www.tudou.com
* YinYueTai http://www.yinyuetai.com

Supported Video Formats
~~~~~~~~~~~~~~~~~~~~~~~

* WebM (\*.webm)
* MP4 (\*.mp4)
* FLV (\*.flv)
* 3GP (\*.3gp)

Installation
------------

#) Install via `Pip <http://www.pip-installer.org/>`_::

    $ pip install you_get
    
   Check if the installation was successful::
    
    $ you-get -V

#) Install via `EasyInstall <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install you_get
    
   Check if the installation was successful::
    
    $ you-get -V

#) Direct download (from https://github.com/soimort/you-get/zipball/master)::
    
    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip
    
   Use the raw script without installation::
    
    $ cd soimort-you-get-*/
    $ ./you-get -V
    
   To install the package into the system path, execute::
    
    $ make install
    
   Or::
    
    > setup.py install
    
   on Windows.
    
   Check if the installation was successful::
    
    $ you-get -V

#) Clone the Git repository (RECOMMENDED!)::

    $ git clone git://github.com/soimort/you-get.git
    
   Use the raw script without installation::
    
    $ cd you-get/
    $ ./you-get -V
    
   To install the package into the system path, execute::
    
    $ make install
    
   Or::
    
    > setup.py install
    
   on Windows.
    
   Check if the installation was successful::
    
    $ you-get -V

Examples (For End-Users)
------------------------

Display the information of the video without downloading::

    $ you-get -i http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download the video::

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download multiple videos::

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M http://www.youtube.com/watch?v=8bQlxQJEzLk

By default, program will skip any video that already exists in the local directory when downloading. If a temporary file (ends with a filename extension ".download") exists, program will resume this download.

To enforce the re-downloading of videos, use '-f' option (this will overwrite any existing video or temporary file, rather than skipping or resuming them)::

    $ you-get -f http://www.youtube.com/watch?v=sGwy8DsUJ4M

Set the output directory of downloaded files::

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

In Python 3.2 (interactive)::

    >>> import you_get
    
    >>> you_get.__version__
    '0.1'
    
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
