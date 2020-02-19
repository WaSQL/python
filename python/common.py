#! python
'''
	modules list
		https://docs.python.org/3/py-modindex.html
'''

import os
import sys
#import dateparser

def isCLI():
	if sys.stdin.isatty():
		return True
	else:
		return False

# def isDate(str):
# 	try:
# 		d=(dateparser.parse(str))
# 		return True
# 	except ValueError:
# 		return False

def echo(str):
	if isCLI():
		print(str,end="\n")
	else:
		print(str,end="<br />\n")

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

def getParentPath(path):
	return os.path.abspath(os.path.join(path, os.pardir))
