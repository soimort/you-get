# -*- Coding:utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
"""
################################################################################
Only for Windows CMD 、PowerShell

Can be compatibale with python2(>2.6)(Care: UniocoedEncodeError)
################################################################################
"""

import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
#由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.


# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_DARKBLUE = 0x10 # dark blue.
BACKGROUND_DARKGREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.



# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

###############################################################

class printColor:
    """
    __exit__:self, exc_type, exc_value, traceback
    """
    def __exit__(self,*args,**kwargs):
        resetColor()

#暗蓝色
#dark blue
class printDarkBlue(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKBLUE)


#暗绿色
#dark green
class printDarkGreen(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKGREEN)


#暗天蓝色
#dark sky blue
class printDarkSkyBlue(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKSKYBLUE)


#暗红色
#dark red
class printDarkRed(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKRED)


#暗粉红色
#dark pink
class printDarkPink(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKPINK)


#暗黄色
#dark yellow
class printDarkYellow(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKYELLOW)


#暗白色
#dark white
class printDarkWhite(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKWHITE)


#暗灰色
#dark gray
class printDarkGray(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_DARKGRAY)


#蓝色
#blue
class printBlue(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_BLUE)


#绿色
#green
class printGreen(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_GREEN)


#天蓝色
#sky blue
class printSkyBlue(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_SKYBLUE)


#红色
#red
class printRed(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_RED)


#粉红色
#pink
class printPink(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_PINK)


#黄色
#yellow
class printYellow(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_YELLOW)


#白色
#white
class printWhite(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_WHITE)


##################################################

#白底黑字
#white bkground and black text
class printWhiteBlack(printColor):
    def __enter__(self):
        set_cmd_text_color(FOREGROUND_BLACK | BACKGROUND_WHITE)


#白底黑字
#white bkground and black text
class printWhiteBlack_2(printColor):
    def __enter__(self):
        set_cmd_text_color(0xf0)



#黄底蓝字
#white bkground and black text
class printYellowRed(printColor):
    def __enter__(self):
        set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)

#原样输出
#write origin text
class printBlank(printColor):
    def __enter__(self):
        pass

################################################################################
# Application layer encapsulation
#
# with print_color('xxx'):
#       print(xxx)
################################################################################
print_map={'darkblue'    : printDarkBlue,
           'darkgreen'   : printDarkGreen,
           'darkskyblue' : printDarkSkyBlue,
           'darkred'     : printDarkRed,
           'darkpink'    : printDarkPink,
           'darkyellow'  : printDarkYellow,
           'darkwhite'   : printDarkWhite,
           'darkgray'    : printDarkGray,

           'blue'        : printBlue,
           'green'       : printGreen,
           'skyblue'     : printSkyBlue,
           'red'         : printRed,
           'pink'        : printPink,
           'yellow'      : printYellow,
           'white'       : printWhite,

           'blank'       : printBlank}



def print_color(color='darkwhite'):
    """

    Args:
        color: default darkwhite/printDarkWhite

    Returns: an printColor instance

    """
    return print_map.get(color,printDarkWhite)()


if __name__ == '__main__':

    with print_color('darkblue'):
        print(u'printDarkBlue:暗蓝色文字\n')

    with print_color('darkgreen'):
        print(u'printDarkGreen:暗绿色文字\n')

    with print_color('darkblue'):
        print(u'printDarkSkyBlue:暗天蓝色文字\n')

    with print_color('darkred'):
        print(u'printDarkRed:暗红色文字\n')

    with print_color('darkpink'):
        print(u'printDarkPink:暗粉红色文字\n')

    with print_color('darkyellow'):
        print(u'printDarkYellow:暗黄色文字\n')

    with print_color('darkwhite'):
        print(u'printDarkWhite:暗白色文字\n')

    with print_color('darkgray'):
        print(u'printDarkGray:暗灰色文字\n')

    with print_color('blue'):
        print(u'printBlue:蓝色文字\n')

    with print_color('green'):
        print(u'printGreen:绿色文字\n')

    with print_color('skyblue'):
        print(u'printSkyBlue:天蓝色文字\n')

    with print_color('red'):
        print(u'printRed:红色文字\n')

    with print_color('pink'):
        print(u'printPink:粉红色文字\n')

    with print_color('yellow'):
        print(u'printYellow:黄色文字\n')

    with print_color('white'):
        print(u'printWhite:白色文字\n')

    with print_color('blank'):
        print(u'printBlank:原生颜色')
    with printWhiteBlack():
        print(u'printWhiteBlack:白底黑字输出\n')

    with printWhiteBlack_2():
        print(u'printWhiteBlack_2:白底黑字输出（直接传入16进制参数）\n')

    with printYellowRed():
        print(u'printYellowRed:黄底红字输出\n')

