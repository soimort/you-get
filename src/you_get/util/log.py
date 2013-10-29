#!/usr/bin/env python

from ..version import __name__

import os, sys

# Is terminal ANSI/VT100 compatible
if os.getenv('TERM') in (
        'xterm',
        'vt100',
        'linux',
        'eterm-color',
    ):
    has_colors = True
else:
    try:
        ppid = os.getppid()
        has_colors = (os.popen('ps -p %d -ocomm=' % ppid).read().strip()
                      == 'emacs')
    except:
        has_colors = False

# ANSI/VT100 escape code
# http://en.wikipedia.org/wiki/ANSI_escape_code
colors = {
    'none': '',
    'reset': '\033[0m',

    'black': '\033[30m',
    'bold-black': '\033[30;1m',
    'dark-gray': '\033[90m',
    'bold-dark-gray': '\033[90;1m',

    'red': '\033[31m',
    'bold-red': '\033[31;1m',
    'light-red': '\033[91m',
    'bold-light-red': '\033[91;1m',

    'green': '\033[32m',
    'bold-green': '\033[32;1m',
    'light-green': '\033[92m',
    'bold-light-green': '\033[92;1m',

    'yellow': '\033[33m',
    'bold-yellow': '\033[33;1m',
    'light-yellow': '\033[93m',
    'bold-light-yellow': '\033[93;1m',

    'blue': '\033[34m',
    'bold-blue': '\033[34;1m',
    'light-blue': '\033[94m',
    'bold-light-blue': '\033[94;1m',

    'magenta': '\033[35m',
    'bold-magenta': '\033[35;1m',
    'light-magenta': '\033[95m',
    'bold-light-magenta': '\033[95;1m',

    'cyan': '\033[36m',
    'bold-cyan': '\033[36;1m',
    'light-cyan': '\033[96m',
    'bold-light-cyan': '\033[96;1m',

    'light-gray': '\033[37m',
    'bold-light-gray': '\033[37;1m',
    'white': '\033[97m',
    'bold-white': '\033[97;1m',
}

def println(message):
    """Prints a log message.
    """
    sys.stderr.write("{0}: {1}\n".format(__name__, message))

def writeln(color, message):
    """Prints a colorful log message.
    """
    if color in colors:
        sys.stderr.write("{0}{1}: {2}{3}\n".format(colors[color], __name__, message, colors['reset']))
    else:
        sys.stderr.write("{0}: {1}\n".format(__name__, message))

def i(message):
    """Sends an info log message.
    """
    if has_colors:
        writeln('white', message)
    else:
        println(message)

def d(message):
    """Sends a debug log message.
    """
    if has_colors:
        writeln('blue', message)
    else:
        println(message)

def w(message):
    """Sends a warning log message.
    """
    if has_colors:
        writeln('yellow', message)
    else:
        println(message)

def e(message):
    """Sends an error log message.
    """
    if has_colors:
        writeln('light-red', message)
    else:
        println(message)

def wtf(message):
    """What a Terrible Failure.
    """
    if has_colors:
        writeln('bold-red', message)
    else:
        println(message)
