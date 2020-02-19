#! python

import os
import sys

import common

if not common.isCLI():
  print("Content-type: text/html; charset=UTF-8;\n\n")

import config

common.echo("hello there")

if common.isWindows():
  common.echo("you are on windows")
else:
  common.echo("you are not on windows")

if common.isCLI():
  common.echo("running from command line")
else:
  common.echo("not running from command line")

# if common.isDate('2019-1d2-22'):
#   print("valid date",end="<br />\n")
# else:
#   print("invalid date",end="<br />\n")
