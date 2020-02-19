#! python
'''
	config.py parses config.xml and builds CONFIG and ALLCONFIG
	References:
		https://www.guru99.com/manipulating-xml-with-python.html
	Installs needed
		pip install xmltodict
		php install pprint
'''

import xmltodict
import os
from pprint import pprint
import common

mypath = os.path.dirname(os.path.realpath(__file__))
parpath = common.getParentPath(mypath)
configfile = parpath+os.path.sep+"config.xml"

with open(configfile) as fd:
    CONFIG = xmltodict.parse(fd.read())

common.echo(configfile)

pprint(CONFIG['hosts']['database'][0])
pprint(CONFIG['hosts']['host'][0])
