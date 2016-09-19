# -*- coding:utf-8 -*-

__all__ = ['chaturbate_download']

import subprocess
from .. import common


def find_player(player):
    maybe_player_path = "/usr/local/bin:"
    import os
    path_env = os.environ.copy()
    path_env["PATH"] = maybe_player_path + path_env["PATH"] 
    p = subprocess.Popen(["/usr/bin/which", player], stdout=subprocess.PIPE, env=path_env)
    p.wait()
    has_player = p.stdout.read()
    return has_player.strip()

def launch_player(player, urls):
    default_player = "vlc"
    player = find_player(default_player)
    if player:
        subprocess.Popen([player, urls[0]])
    else:
        #try to use builtin player. QuickTime Player MacOs Only
        import sys
        if sys.platform == "darwin":
            apple_script = 'tell application "QuickTime Player" to Open Url "%s"' % urls[0]
            subprocess.Popen(["/usr/bin/osascript", "-e", apple_script])
        else:
            raise Exception("There is no available player!")


def chaturbate_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = common.get_content(url)
    hls_url = common.r1("'(.*\.m3u8)'", html)
    title =common.r1("<title>Chat with ([A-Za-z0-9_]*).*</title>", html)
    common.launch_player = launch_player
    common.print_info(site_info, title, 'm3u8', float('inf'))


    if not info_only:
        common.download_url_ffmpeg(hls_url, title, 'mp4', None, output_dir = output_dir, merge = merge)

site_info = "chaturbate.com"
download = chaturbate_download
download_playlist = common.playlist_not_supported('chaturbate')
