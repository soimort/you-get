#!/usr/bin/env python

import fcntl, termios, struct

def get_terminal_size():
    """Get (width, height) of the current terminal."""
    try:
        return struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
    except:
        return (40, 80)
