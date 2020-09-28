#! python
"""
References
    https://www.php2python.com/

"""
import os
import sys
#import common.py
try:
    import common
    import requests
    from urllib.parse import urlparse, parse_qs, parse_qsl
    import config
    import db
    import re
    from importlib import import_module
    #common.echo("common imported")
except ImportError as err:
    print("Content-type: text/plain; charset=UTF-8;\n\n")
    sys.exit(err)
#header
if not common.isCLI():
    print("Content-type: text/html; charset=UTF-8;\n\n")
#url
HTTP_HOST = 'localhost'
if 'HTTP_HOST' in os.environ:
    HTTP_HOST = os.environ['HTTP_HOST']
url = '//'+HTTP_HOST
if 'REDIRECT_URL' in os.environ:
    url+=os.environ['REDIRECT_URL']
    if 'QUERY_STRING' in os.environ:
        url+='?'+os.environ['QUERY_STRING']
else:
    url+=os.environ['REQUEST_URI']

# REQUEST setup
parsed_url = urlparse(url)
REQUEST = dict(parse_qsl(parsed_url.query))
#initial some global variables
PAGE = {}
TEMPLATE = {}
#view a page
if '_view' in REQUEST:
    view = REQUEST['_view']
    #build query using python3+ f strings
    query="select * from _pages where name='{}' or permalink='{}'".format(view,view);
    recs = db.queryResults(config.CONFIG['database'],query,{})
    if type(recs) in (tuple, list):
        for rec in recs:
            #SET PAGE
            for rk in rec:
                if isinstance(rec[rk],str):
                    PAGE[rk]=rec[rk].strip()
                else:
                    PAGE[rk]=rec[rk]
            #set common.VIEWS
            common.parseViews(rec['body'])
            body = rec['body']
            #check for functions
            if 'functions' in rec and len(rec['functions']) > 0:
                compileString=''
                compileString = rec['functions'] + os.linesep + os.linesep
                compiledCodeBlock = compile(compileString, '<string>', 'exec')
                eval(compiledCodeBlock)
            #Check for controller
            if 'controller' in rec and len(rec['controller']) > 0:
                compileString=''
                compileString = rec['controller'] + os.linesep + os.linesep
                compiledCodeBlock = compile(compileString, '<string>', 'exec')
                eval(compiledCodeBlock)
            #process page views set
            if not bool(common.VIEW.keys):
                common.createView('default',rec['body'])

            for viewname in common.VIEW:
                rtn = common.parseCodeBlocks(common.VIEW[viewname]).strip()
                repstr="<view:{}>{}</view:{}>".format(viewname,common.VIEW[viewname],viewname)
                body=common.str_replace(repstr,rtn,body)
            #remove other views
            views = common.parseViewsOnly(body)
            for viewname in views:
                repstr="<view:{}>{}</view:{}>".format(viewname,views[viewname],viewname)
                body=common.str_replace(repstr,'',body)
            print(body)
            break
    else:
        print(recs)