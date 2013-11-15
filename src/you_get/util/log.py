#!/usr/bin/env python

from ..version import __name__

import os, sys, subprocess

# Is terminal ANSI/VT100 compatible
if os.getenv('TERM') in (
        'xterm',
        'vt100',
        'linux',
        'eterm-color',
        'screen',
    ):
    has_colors = True
else:
    try:
        # Eshell
        ppid = os.getppid()
        has_colors = (subprocess.getoutput('ps -p %d -ocomm=' % ppid)
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

def underlined(text):
    """Returns an underlined text.
    """
    return "\33[4m%s\33[24m" % text if has_colors else text

def println(text, color=None, ostream=sys.stdout):
    """Prints a text line to stream.
    """
    if has_colors and color in colors:
        ostream.write("{0}{1}{2}\n".format(colors[color], text, colors['reset']))
    else:
        ostream.write("{0}\n".format(text))

def printlog(message, color=None, ostream=sys.stderr):
    """Prints a log message to stream.
    """
    if has_colors and color in colors:
        ostream.write("{0}{1}: {2}{3}\n".format(colors[color], __name__, message, colors['reset']))
    else:
        ostream.write("{0}: {1}\n".format(__name__, message))

def i(message, ostream=sys.stderr):
    """Sends an info log message.
    """
    printlog(message,
             None,
             ostream=ostream)

def d(message, ostream=sys.stderr):
    """Sends a debug log message.
    """
    printlog(message,
             'blue' if has_colors else None,
             ostream=ostream)

def w(message, ostream=sys.stderr):
    """Sends a warning log message.
    """
    printlog(message,
             'yellow' if has_colors else None,
             ostream=ostream)

def e(message, ostream=sys.stderr):
    """Sends an error log message.
    """
    printlog(message,
             'bold-yellow' if has_colors else None,
             ostream=ostream)

def wtf(message, ostream=sys.stderr):
    """What a Terrible Failure.
    """
    printlog(message,
             'bold-red' if has_colors else None,
             ostream=ostream)
