#!/usr/bin/env python

def get_terminal_size():
    """Get (width, height) of the current terminal."""
    try:
        import fcntl, termios, struct # fcntl module only available on Unix
        return struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
    except:
        return (40, 80)
