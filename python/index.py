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
    if not common.isCLI():
        print("Content-type: text/html; charset=UTF-8;\n\n")
    #common.echo("common imported")
except ImportError as err:
    print("Content-type: text/plain; charset=UTF-8;\n\n")
    sys.exit(err)

#import requests
try:
    import requests
except ImportError as err:
    sys.exit(err)

#import urlparse
try:
    from urllib.parse import urlparse, parse_qs
except ImportError as err:
    sys.exit(err)


#import config 
try:
    import config
except ImportError as err:
    sys.exit(err)

#import db
try:
    import db
except ImportError as err:
    print(err)
    sys.exit(err)
url = '//'+os.environ['HTTP_HOST']+os.environ['REQUEST_URI']
parsed_url = urlparse(url)
REQUEST = parse_qs(parsed_url.query)
#common.printValue(parsed_url)
common.printValue(REQUEST)
common.printValue('<HR>')
#test
recs = db.queryResults('wasql5',"select code,name from states where country='US'",{});
common.printValue(recs)
#check to see if results is an array.
if type(recs) in (tuple, list):
    for rec in recs:
        print(rec)
        for key in rec.keys():
            print(rec[key])
            break
        break
else:
    print(recs)