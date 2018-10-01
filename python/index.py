#!/usr/bin/env python
print("Content-type: text/html")
print("")
#cgitb prints errors to the browser
import cgitb
cgitb.enable()
#untangle loads xml into an object -- https://github.com/stchris/untangle -- pip install untangle
import untangle
CONFIG = untangle.parse('../config.xml')
print (CONFIG.__dict__)

# print("<html><head>")
# print("")
# print("</head><body>")
# print("python port of WaSQL Web Development Platform - in development")
# print("</body></html>")