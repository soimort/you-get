# Fish completion definition for you-get.

complete -c you-get -s V -l version -d 'print version and exit'
complete -c you-get -s h -l help -d 'print help and exit'
complete -c you-get -s i -l info -d 'print extracted information'
complete -c you-get -s u -l url -d 'print extracted information'
complete -c you-get -l json -d 'print extracted URLs in JSON format'
complete -c you-get -s n -l no-merge -d 'do not merge video parts'
complete -c you-get -l no-caption -d 'do not download captions'
complete -c you-get -s f -l force -d 'force overwrite existing files'
complete -c you-get -s F -l format -x -d 'set video format to the specified stream id'
complete -c you-get -s O -l output-filename -d 'set output filename' \
         -x -a '(__fish_complete_path (commandline -ct) "output filename")'
complete -c you-get -s o -l output-dir  -d 'set output directory' \
         -x -a '(__fish_complete_directories (commandline -ct) "output directory")'
complete -c you-get -s p -l player -x -d 'stream extracted URL to the specified player'
complete -c you-get -s c -l cookies -d 'load cookies.txt or cookies.sqlite' \
         -x -a '(__fish_complete_path (commandline -ct) "cookies.txt or cookies.sqlite")'
complete -c you-get -s x -l http-proxy -x -d 'use the specified HTTP proxy for downloading'
complete -c you-get -s y -l extractor-proxy -x -d 'use the specified HTTP proxy for extraction only'
complete -c you-get -l no-proxy -d 'do not use a proxy'
complete -c you-get -s t -l timeout -x -d 'set socket timeout'
complete -c you-get -s d -l debug -d 'show traceback and other debug info'
