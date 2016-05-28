# -*- Coding:utf-8 -*-
#!/usr/bin/env python3
"""
################################################################################
Establish a Unified Color print across all kinds of os
################################################################################
"""

from .__init__ import iswin,islinux

if islinux():
    from . import color_sh as sh
elif iswin():
    from . import color_cmd as cmd


def printWhite(obj):
    if iswin():
        with cmd.printWhite():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'white'))

    else:
        print(obj)
def printDarkPink(obj):
    if iswin():
        with cmd.printDarkPink():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'purple'))

    else:
        print(obj)

def printBlue(obj):
    """
    Belive it ,It's an ugly print-color.
    Blue makes you blue :(
    :param obj:
    :return:
    """
    if iswin():
        with cmd.printBlue():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'blue'))

    else:
        print(obj)


def printDarkRed(obj):
    if iswin():
        with cmd.printDarkRed():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'red'))

    else:
        print(obj)


def printDarkSkyBlue(obj):
    if iswin():
        with cmd.printDarkSkyBlue():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'cyan'))

    else:
        print(obj)

def printDarkGreen(obj):
    if iswin():
        with cmd.printDarkGreen():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'green'))

    else:
        print(obj)

def printDarkYellow(obj):
    if iswin():
        with cmd.printDarkYellow():
            print(obj)
    elif islinux():
        print(sh.UseStyle(obj,'yellow'))

    else:
        print(obj)

################################################################################
# Application layer encapsulation
#
# 4 Kind of Print:
#
# print Common Information         : print_info
# print Succeed Information        : print_ok
# print Warinng Information        : print_warn or print_warning
# print Error Information          : print_err or print_error
#
#You can also configure them with color_dict and print_map
################################################################################
color_dict={'green' : printDarkGreen,
            'skyblue' : printDarkSkyBlue,
            'yellow' : printDarkYellow,
            'red' : printDarkRed,
            'blue':printBlue,
            'white':printWhite,
            'purple':printDarkPink}

print_map={'info' : color_dict['skyblue'],
           'ok' : color_dict['green'],
           'warning' : color_dict['yellow'],
           'error' : color_dict['red']}

def print_info(obj):print_map['info'](obj)
def print_ok(obj):print_map['ok'](obj)

def print_warning(obj):print_map['warning'](obj)
def print_warn(obj): print_warning(obj) # print_warning is too long

def print_error(obj):print_map['error'](obj)
def print_err(obj):print_error(obj) #print_error is too long



if __name__ == '__main__':
    print('isLinux?%r'%islinux())
    print('isWindows?%r'%iswin())

    printDarkRed({'a':1,'b':2})
    printDarkGreen([1,2,3])
    printDarkSkyBlue((1,2,3))
    printDarkYellow({1,2,3})

    printDarkPink('abc'+'def')
    printBlue(printBlue)
    printWhite('White Char')

    print_info('info')
    print_ok('ok means that exec action succeed')
    print_warning('warning')
    print_warning('print_warning is too long')
    print_error('error')
    print_err('print_error is too long')
