# -*- Coding:utf-8 -*-
#!/usr/bin/env python3
"""
################################################################################
Establish a Unified Color print across all kinds of os

However, you should care about that
         we only implemented 8^1=8 kind of basic color in color_sh
################################################################################
"""

from .__init__ import iswin,islinux

if islinux():
    from . import color_sh as sh
elif iswin():
    from . import color_cmd as cmd

def _remove_key(dic,keys):
    return {_key:dic[_key] for _key in dic if _key not in set(keys)}

def print_color(*objs,**kwargs):

    _end=kwargs.get('end' ,'\n')
    _sep=kwargs.get('sep' ,' ')
    _color=kwargs.get('color','blank')
    kwargs=_remove_key(kwargs,['end','sep','color'])

    if iswin():
        with cmd.print_color(color=_color):
            [print(obj, end=_sep, sep='',**kwargs) for obj in objs]
            print(end=_end)

    elif islinux():
        [print(sh.UseStyle(obj,fore=_color), end=_sep, sep='',**kwargs)
         for obj in objs]

        print(end=_end)

    else:
        [print(obj, end=_sep, sep='',**kwargs) for obj in objs]
        print(end=_end)

def printWhite(*objs,**kwargs):
    print_color(*objs,color='white',**kwargs)


def printDarkPink(*objs,**kwargs):
    print_color(*objs,color='darkpink',**kwargs)

def printBlue(*objs,**kwargs):
    """
    Belive it ,It's an ugly print-color.
    Blue makes you blue :(
    :param obj:
    :return:
    """
    print_color(*objs,color='blue',**kwargs)

def printDarkRed(*objs,**kwargs):
    print_color(*objs,color='darkred',**kwargs)


def printDarkSkyBlue(*objs,**kwargs):
    print_color(*objs,color='darkskyblue',**kwargs)

def printDarkGreen(*objs,**kwargs):
    print_color(*objs,color='darkgreen',**kwargs)

def printDarkYellow(*objs,**kwargs):
    print_color(*objs,color='darkyellow',**kwargs)

def printBlank(*objs,**kwargs):
    print_color(*objs,color='blank',**kwargs)

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
color_dict={'green'       : printDarkGreen,
            'darkskyblue' : printDarkSkyBlue,
            'yellow'      : printDarkYellow,
            'red'         : printDarkRed,
            'blue'        : printBlue,
            'white'       : printWhite,
            'purple'      : printDarkPink}

print_map={'info'    : color_dict['darkskyblue'],
           'ok'      : color_dict['green'],
           'warning' : color_dict['yellow'],
           'error'   : color_dict['red']}

def print_info(*objs,**kwargs):print_map['info'](*objs,**kwargs)
def print_ok(*objs,**kwargs):print_map['ok'](*objs,**kwargs)

def print_warning(*objs,**kwargs):print_map['warning'](*objs,**kwargs)
def print_warn(*objs,**kwargs): print_warning(*objs,**kwargs) # print_warning is too long

def print_error(*objs,**kwargs):print_map['error'](*objs,**kwargs)
def print_err(*objs,**kwargs):print_error(*objs,**kwargs) #print_error is too long



if __name__ == '__main__':
    print('isLinux?%r'%islinux())
    print('isWindows?%r'%iswin())

    printDarkRed({'a':1,'b':2}, {'c':3}, end='')
    printDarkGreen([1,2,3], 4, sep='*', end='\n')
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
