#!/usr/bin/env python

from platform import system

def detect_os():
    """Detect operating system.
    """

    # Inspired by:
    # https://github.com/scivision/pybashutils/blob/78b7f2b339cb03b1c37df94015098bbe462f8526/pybashutils/windows_linux_detect.py

    syst = system().lower()
    os = 'unknown'

    if 'cygwin' in syst:
        os = 'cygwin'
    elif 'darwin' in syst:
        os = 'mac'
    elif 'linux' in syst:
        os = 'linux'
        # detect WSL https://github.com/Microsoft/BashOnWindows/issues/423
        try:
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    os = 'wsl'
        except: pass
    elif 'windows' in syst:
        os = 'windows'
    elif 'bsd' in syst:
        os = 'bsd'

    return os
