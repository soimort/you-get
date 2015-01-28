#!/usr/bin/env python

import platform
import sys
from .strings import safe_chars

def legitimize(text, os=platform.system()):
    """Converts a string to a valid filename.
    """

    # POSIX systems
    text = text.translate({
        0: None,
        ord('/'): '-',
    })

    if os == 'Windows':
        # Windows (non-POSIX namespace)
        text = text.translate({
            # Reserved in Windows VFAT and NTFS
            ord(':'): '-',
            ord('*'): '-',
            ord('?'): '-',
            ord('\\'): '-',
            ord('|'): '-',
            ord('\"'): '\'',
            # Reserved in Windows VFAT
            ord('+'): '-',
            ord('<'): '-',
            ord('>'): '-',
            ord('['): '(',
            ord(']'): ')',
        })
    else:
        # *nix
        if os == 'Darwin':
            # Mac OS HFS+
            text = text.translate({
                ord(':'): '-',
            })

        # Remove leading .
        if text.startswith("."):
            text = text[1:]

    return text

def get_filename(basename, ext, id=None, part=None, encoding=sys.getfilesystemencoding(), **kwargs):
    safe_basename = safe_chars(basename, encoding=encoding)
    if safe_basename != basename and id is not None:
        safe_basename = safe_chars('%s - %s' % (basename, id), encoding=encoding)
    safe_basename = safe_basename[:82] # Trim to 82 Unicode characters long
    if part is not None:
        safe_basename = '%s[%02d]' % (safe_basename, part)
    return legitimize('%s.%s' % (safe_basename, ext), **kwargs)