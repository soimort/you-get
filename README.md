# You-Get

一个Python 3的YouTube/优酷视频下载脚本。

### Python版本

Python 3.x

### 说明

基于优酷下载脚本[iambus/youku-lixian](https://github.com/iambus/youku-lixian)用Python 3改写而成，增加了以下功能：

* 支持YouTube
* 支持断点续传
* 可设置HTTP代理

### 支持的站点（持续更新中）

目前根据本人需求，仅实现了对有限几个视频站点的支持，以后会继续增加（・∀・）

* YouTube <http://www.youtube.com>
* 音悦台 <http://www.yinyuetai.com>
* 优酷 <http://www.youku.com>
* 土豆 <http://www.tudou.com>

### 输出视频格式

* WebM (*.webm)
* MP4 (*.mp4)
* FLV (*.flv)
* 3GP (*.3gp)

对于YouTube，程序将下载画质最高的[编码格式](http://en.wikipedia.org/wiki/Youtube#Quality_and_codecs)。

### 如何下载视频

（以下命令均以Linux shell为例……Windows用户请自行脑补正确的命令格式）

显示视频信息，但不进行下载（`-i`或`--info`选项）：

    $ ./you-get -i http://www.yinyuetai.com/video/463772

下载视频：

    $ ./you-get http://www.yinyuetai.com/video/463772

下载多个视频：

    $ ./you-get http://www.yinyuetai.com/video/463772 http://www.yinyuetai.com/video/471500

若当前目录下已有与视频标题同名的文件，下载时会自动跳过。若有同名的`.download`临时文件，程序会从上次中断处开始下载。
如要强制重新下载该视频，可使用`-f`（`--force`）选项：

    $ ./you-get -f http://www.yinyuetai.com/video/463772

`-l`（`--playlist`）选项用于下载播放列表（只对某些网站适用）：

    $ ./you-get -l http://www.youku.com/playlist_show/id_5344313.html

指定视频文件的下载目录：

    $ ./you-get -o ~/Downloads http://www.yinyuetai.com/video/463772

显示详细帮助：

    $ ./you-get -h

### 如何设置代理

默认情况下，Python自动使用系统的代理配置。可以通过环境变量`http_proxy`来设置系统的HTTP代理。

`-x`（`--http-proxy`）选项用于手动指定You-Get所使用的HTTP代理。例如：GoAgent的代理服务器是`http://127.0.0.1:8087`，则使用该代理下载某YouTube视频的命令是：

    $ ./you-get -x 127.0.0.1:8087 http://www.youtube.com/watch?v=KbtO_Ayjw0M

Windows下的自由门等翻墙软件会自动设置系统全局代理，因此无需指定HTTP代理即可下载YouTube视频：

    $ ./you-get http://www.youtube.com/watch?v=KbtO_Ayjw0M

如果不希望程序在下载过程中使用任何代理（包括系统的代理配置），可以显式地指定`--no-proxy`选项：

    $ ./you-get --no-proxy http://v.youku.com/v_show/id_XMjI0ODc1NTc2.html

### 断点续传

下载未完成时意外中止（因为网络中断或程序被强行终止等），在目标路径中会有一个扩展名为`.download`的临时文件。

下次运行只要在目标路径中找到相应的`.download`临时文件，程序会自动从中断处继续下载。（除非指定了`-f`选项）

### 使用Python 2？

优酷等国内视频网站的下载，请移步：[iambus/youku-lixian](https://github.com/iambus/youku-lixian)

YouTube等国外视频网站的下载，请移步：[rg3/youtube-dl](https://github.com/rg3/youtube-dl)

### 许可证

源码在MIT License下发布。
