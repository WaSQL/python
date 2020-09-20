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
    from importlib import import_module
    #common.echo("common imported")
except ImportError as err:
    print("Content-type: text/plain; charset=UTF-8;\n\n")
    sys.exit(err)
#header
if not common.isCLI():
    print("Content-type: text/html; charset=UTF-8;\n\n")
#url
url = '//'+os.environ['HTTP_HOST']
if 'REDIRECT_URL' in os.environ:
    url+=os.environ['REDIRECT_URL']
    if 'QUERY_STRING' in os.environ:
        url+='?'+os.environ['QUERY_STRING']
else:
    url+=os.environ['REQUEST_URI']

# REQUEST setup
parsed_url = urlparse(url)
REQUEST = dict(parse_qsl(parsed_url.query))
#view a page
if '_view' in REQUEST:
    query="select * from _pages where name='{}' or permalink='{}'".format(REQUEST['_view'],REQUEST['_view'])
    recs = db.queryResults(config.CONFIG['database'],query,{});
    if type(recs) in (tuple, list):
        for rec in recs:
            if 'functions' in rec and len(rec['functions']) > 0:
                filename = 'd:/wasql.py/python/page.py'
                modname='page'
                #common.setFileContents(filename,'#! python'+os.linesep+rec['functions'])
                import page

                #os.remove(filename)
            eval(rec['body'])
            break
    else:
        print(recs)

