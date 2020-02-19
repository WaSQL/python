#! python
'''
	config.py parses config.xml and builds CONFIG and ALLCONFIG
	References:
		https://www.guru99.com/manipulating-xml-with-python.html
'''

import xml.dom.minidom

CONFIG = xml.dom.minidom.parse("d:/wasql/config.xml")

print(CONFIG)