# You-Get

[You-Get](https://github.com/soimort/you-get) is a video downloader runs on Python 3. It aims at easing the download of videos on [YouTube](http://www.youtube.com), [Youku](http://www.youku.com)/[Tudou](http://www.tudou.com) (biggest online video providers in China), etc., in one tool.

See the project homepage <http://www.soimort.org/you-get> for further documentation.

Fork me on GitHub: <https://github.com/soimort/you-get>

## Features

### Supported Sites (UPDATING!)

* YouTube <http://www.youtube.com>
* Youku <http://www.youku.com>
* Tudou <http://www.tudou.com>
* YinYueTai <http://www.yinyuetai.com>

### Supported Video Formats

* WebM (*.webm)
* MP4 (*.mp4)
* FLV (*.flv)
* 3GP (*.3gp)

## Installation

### 1. Install via [Pip](http://www.pip-installer.org/):

    $ pip install you_get
    
   Check if the installation was successful:
    
    $ you-get -V

### 2. Install via [EasyInstall](http://pypi.python.org/pypi/setuptools):

    $ easy_install you_get
    
   Check if the installation was successful:
    
    $ you-get -V

### 3. Direct download (from <https://github.com/soimort/you-get/zipball/master>):
    
    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip
    
   Use the raw script without installation:
    
    $ cd soimort-you-get-*/
    $ ./you-get -V
    
   To install the package into the system path, execute:
    
    $ make install
    
   Or:
    
    > setup.py install
    
   on Windows.
    
   Check if the installation was successful:
    
    $ you-get -V

### 4. Clone the Git repository (RECOMMENDED!):

    $ git clone git://github.com/soimort/you-get.git
    
   Use the raw script without installation:
    
    $ cd you-get/
    $ ./you-get -V
    
   To install the package into the system path, execute:
    
    $ make install
    
   Or:
    
    > setup.py install
    
   on Windows.
    
   Check if the installation was successful:
    
    $ you-get -V

## Examples (For End-Users)

Display the information of the video without downloading:

    $ you-get -i http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download the video:

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M

Download multiple videos:

    $ you-get http://www.youtube.com/watch?v=sGwy8DsUJ4M http://www.youtube.com/watch?v=8bQlxQJEzLk

By default, program will skip any video that already exists in the local directory when downloading. If a temporary file (ends with a filename extension ".download") exists, program will resume this download.

To enforce the re-downloading of videos, use '-f' option (this will overwrite any existing video or temporary file, rather than skipping or resuming them):

    $ you-get -f http://www.youtube.com/watch?v=sGwy8DsUJ4M

Set the output directory of downloaded files:

    $ you-get -o ~/Downloads http://www.youtube.com/watch?v=sGwy8DsUJ4M

Use a specific HTTP proxy for downloading:

    $ you-get -x 127.0.0.1:8087 http://www.youtube.com/watch?v=sGwy8DsUJ4M

By default, Python will apply the system proxy settings (i.e. environment variable $http_proxy). To cancel the use of proxy, use '--no-proxy' option:

    $ you-get --no-proxy http://www.youtube.com/watch?v=sGwy8DsUJ4M

## Command-Line Options

For a complete list of all available options, see:

    $ you-get --help

## Examples (For Developers)

In Python 3.2 (interactive):

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

## API Reference

See source code.

## License

You-Get is licensed under the [MIT license](https://raw.github.com/soimort/you-get/master/LICENSE.txt).



***



# You-Get - 中文说明

[You-Get](https://github.com/soimort/you-get)是一个基于Python 3的视频下载工具。之所以写它的主要原因是，我找不到一个现成的下载工具能够同时支持[YouTube](http://www.youtube.com/)和[优酷](http://www.youku.com/)；而且，几乎所有以前的视频下载程序都是基于Python 2的。

## 特点

### 说明

You-Get基于优酷下载脚本[iambus/youku-lixian](https://github.com/iambus/youku-lixian)用Python 3改写而成，增加了以下功能：

* 支持YouTube
* 支持断点续传
* 可设置HTTP代理

### 支持的站点（持续更新中）

目前根据本人需求，仅实现了对有限几个视频站点的支持，以后会继续增加（・∀・）

* YouTube <http://www.youtube.com>
* 优酷 <http://www.youku.com>
* 土豆 <http://www.tudou.com>
* 音悦台 <http://www.yinyuetai.com>

### 输出视频格式

* WebM (*.webm)
* MP4 (*.mp4)
* FLV (*.flv)
* 3GP (*.3gp)

对于YouTube，程序将下载画质最高的[编码格式](http://en.wikipedia.org/wiki/Youtube#Quality_and_codecs)。

## 安装方法

（以下命令均以Linux shell为例）

### 1. 通过[Pip](http://www.pip-installer.org/)安装:

    $ pip install you_get
    
   检查安装是否成功：
    
    $ you-get -V

### 2. 通过[EasyInstall](http://pypi.python.org/pypi/setuptools)安装：

    $ easy_install you_get
    
   检查安装是否成功：
    
    $ you-get -V

### 3. 直接下载（从<https://github.com/soimort/you-get/zipball/master>）：
    
    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip
    
   在不安装的情况下直接使用脚本：
    
    $ cd soimort-you-get-*/
    $ ./you-get -V
    
   若要将Python package安装到系统默认路径，执行：
    
    $ make install
    
   或：（适用于Windows）
    
    > setup.py install
    
   检查安装是否成功：
    
    $ you-get -V

### 4. 从Git安装（推荐）:

    $ git clone git://github.com/soimort/you-get.git
    
   在不安装的情况下直接使用脚本：
    
    $ cd you-get/
    $ ./you-get -V
    
   若要将Python package安装到系统默认路径，执行：
    
    $ make install
    
   或：（适用于Windows）
    
    > setup.py install
    
   检查安装是否成功：
    
    $ you-get -V

## 使用方法示例

### 如何下载视频

显示视频信息，但不进行下载（`-i`或`--info`选项）：

    $ you-get -i http://www.yinyuetai.com/video/463772

下载视频：

    $ you-get http://www.yinyuetai.com/video/463772

下载多个视频：

    $ you-get http://www.yinyuetai.com/video/463772 http://www.yinyuetai.com/video/471500

若当前目录下已有与视频标题同名的文件，下载时会自动跳过。若有同名的`.download`临时文件，程序会从上次中断处开始下载。
如要强制重新下载该视频，可使用`-f`（`--force`）选项：

    $ you-get -f http://www.yinyuetai.com/video/463772

`-l`（`--playlist`）选项用于下载播放列表（只对某些网站适用）：

    $ you-get -l http://www.youku.com/playlist_show/id_5344313.html

指定视频文件的下载目录：

    $ you-get -o ~/Downloads http://www.yinyuetai.com/video/463772

显示详细帮助：

    $ you-get -h

### 如何设置代理

默认情况下，Python自动使用系统的代理配置。可以通过环境变量`http_proxy`来设置系统的HTTP代理。

`-x`（`--http-proxy`）选项用于手动指定You-Get所使用的HTTP代理。例如：GoAgent的代理服务器是`http://127.0.0.1:8087`，则使用该代理下载某YouTube视频的命令是：

    $ you-get -x 127.0.0.1:8087 http://www.youtube.com/watch?v=KbtO_Ayjw0M

Windows下的自由门等翻墙软件会自动设置系统全局代理，因此无需指定HTTP代理即可下载YouTube视频：

    $ you-get http://www.youtube.com/watch?v=KbtO_Ayjw0M

如果不希望程序在下载过程中使用任何代理（包括系统的代理配置），可以显式地指定`--no-proxy`选项：

    $ you-get --no-proxy http://v.youku.com/v_show/id_XMjI0ODc1NTc2.html

### 断点续传

下载未完成时意外中止（因为网络中断或程序被强行终止等），在目标路径中会有一个扩展名为`.download`的临时文件。

下次运行只要在目标路径中找到相应的`.download`临时文件，程序会自动从中断处继续下载。（除非指定了`-f`选项）

## 使用Python 2？

优酷等国内视频网站的下载，请移步：[iambus/youku-lixian](https://github.com/iambus/youku-lixian)

YouTube等国外视频网站的下载，请移步：[rg3/youtube-dl](https://github.com/rg3/youtube-dl)

## 许可证

You-Get在[MIT License](https://raw.github.com/soimort/you-get/master/LICENSE.txt)下发布。
