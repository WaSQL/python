#! python
'''
    modules list
        https://docs.python.org/3/py-modindex.html
'''

import os
import sys
import pprint
#import dateparser
def echo(str):
    if isCLI():
        print(str,end="\n")
    else:
        print(str,end="<br />\n")

def getParentPath(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def hostname():
    return os.environ['HTTP_HOST']

def isCLI():
    if sys.stdin.isatty():
        return True
    else:
        return False 

def isWindows():
    if sys.platform == 'win32':
        return True
    elif sys.platform == 'win32':
        return True
    elif sys.platform == 'win64':
        return True
    elif os.name == 'nt':
        return True
    else:
        return False

def nl2br(string, is_xhtml= True ):
    if is_xhtml:
        return string.replace('\n','<br />\n')
    else :
        return string.replace('\n','<br>\n')

def printValue(obj):
    pprint.pprint(obj)






