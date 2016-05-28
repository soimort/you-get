# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Provide Color Support for all kinds of shell Stdio
 main API :
     color.color_dict
     color.print_map

     color.print_info
     color.print_ok
     color.print_warn or print_warning
     color.print_err or print_error
################################################################################
"""

import platform
def iswin():
    return platform.platform().upper().startswith('WIN')

def islinux():
    return platform.platform().upper().startswith('LINUX')