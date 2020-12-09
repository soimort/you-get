#!/usr/bin/env python

from .os import detect_os

def legitimize(text, os=detect_os()):
    """Converts a string to a valid filename.
    """

    # POSIX systems
    text = text.translate({
        0: None,
        ord('/'): '-',
        ord('|'): '-',
    })

    # FIXME: do some filesystem detection
    if os == 'windows' or os == 'cygwin' or os == 'wsl':
        # Windows (non-POSIX namespace)
        text = text.translate({
            # Reserved in Windows VFAT and NTFS
            ord(':'): '-',
            ord('*'): '-',
            ord('?'): '-',
            ord('\\'): '-',
            ord('\"'): '\'',
            # Reserved in Windows VFAT
            ord('+'): '-',
            ord('<'): '-',
            ord('>'): '-',
            ord('['): '(',
            ord(']'): ')',
            ord('\t'): ' ',
        })
    else:
        # *nix
        if os == 'mac':
            # Mac OS HFS+
            text = text.translate({
                ord(':'): '-',
            })

        # Remove leading .
        if text.startswith("."):
            text = text[1:]

    text = text[:80] # Trim to 82 Unicode characters long
    return text
