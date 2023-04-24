from ..common import main

# TODO(Alex Potapov): structure the exact arguments.
# Probably need to omit initialization of args entry if option is ommited (remove `args[...] = None/False`)
def you_get_exec(**kwargs):
    args = {}

    # download
    args['--no-merge'] = False
    args['--no-caption'] = True
    args['--postfix'] = False
    args['--prefix'] = None
    args['--force'] = False
    args['--skip-existing-file-size-check'] = False
    args['--format'] = None
    args['--output-filename'] = None
    args['--output-dir'] = '.'
    args['--player'] = None
    args['--cookies'] = None
    args['--timeout'] = 600
    args['--debug'] = False
    args['--input-file'] = None
    args['--password'] = None
    args['--playlist'] = False
    args['--auto-rename'] = False
    args['--insecure'] = False
    args['--stream'] = False
    args['--itag'] = False
    args['--m3u8'] = False
    args['URL'] = ''

    # playlist
    args['--first'] = None
    args['--last'] = None
    args['--size'] = None

    # proxy
    args['--http-proxy'] = None
    args['--extractor-proxy'] = None
    args['--no-proxy'] = False
    args['--socks-proxy'] = None

    main(**args)