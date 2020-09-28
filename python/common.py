#! python
'''
    modules list
        https://docs.python.org/3/py-modindex.html
'''
try:
    import os
    import sys
    import pprint
    import re
    import io
    from math import sin, cos, sqrt, atan2, radians
    import subprocess
    from datetime import datetime
    import time as ttime
except ImportError as err:
    sys.exit(err)

VIEWS = {}
VIEW = {}
#import dateparser

def buildDir(path,mode=0o777,recurse=True):
    if recurse:
        return os.makedirs(path,mode)
    else:
        return os.mkdir(path,mode)

def buildOnLoad(str='',img='/wfiles/clear.gif',width=1,height=1):
    return f'<img class="w_buildonload" src="{img}" alt="onload functions" width="{width}" height="{height}" style="border:0px;" onload="eventBuildOnLoad();" data-onload="{str}">'

def calculateDistance(lat1, lon1, lat2, lon2, unit='M'):
    #Python, all the trig functions use radians, not degrees
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(abs(lat1))
    lon1 = radians(abs(lon1))
    lat2 = radians(abs(lat2))
    lon2 = radians(abs(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    #miles
    if unit == 'M':
        miles = distance * 0.621371;
        return miles
    else:
        return distance

def cmdResults(cmd,args='',dir='',timeout=0):
    result = subprocess.run([cmd, args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.decode('utf-8')
    
def echo(str):
    if isCLI():
        print(str,end="\n")
    else:
        print(str,end="<br />\n")

def setFileContents(filename,data):
    f = open(filename, 'w')
    f.write(data)
    f.close()

def evalPython(str):
    #point stdout to a variable
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    #compile
    compiledCodeBlock = compile(str, '<string>', 'exec')
    rtn = eval(compiledCodeBlock)
    #point stdout back
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    #return
    return output

def formatPhone(phone_number):
    clean_phone_number = re.sub('[^0-9]+', '', phone_number)
    formatted_phone_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]
    return formatted_phone_number

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

def parseViews(str):
    global VIEWS
    VIEWS = {}
    matches = re.findall(r'<view:(.*?)>(.+?)</view:\1>', str,re.MULTILINE|re.IGNORECASE|re.DOTALL)
    for (viewname,viewbody) in matches:
        VIEWS[viewname]=viewbody
    return True

def parseViewsOnly(str):
    views = {}
    matches = re.findall(r'<view:(.*?)>(.+?)</view:\1>', str,re.MULTILINE|re.IGNORECASE|re.DOTALL)
    for (viewname,viewbody) in matches:
        views[viewname]=viewbody
    return views

def parseCodeBlocks(str):
    matches = re.findall(r'<\?=(.*?)\?>', str,re.MULTILINE|re.IGNORECASE|re.DOTALL)
    for match in matches:
        #add our imports: common, db, re,
        evalstr = 'import common'+os.linesep
        evalstr += 'import config'+os.linesep
        evalstr += 'import db'+os.linesep
        evalstr += 'import re'+os.linesep
        evalstr += os.linesep+"print({})".format(match)
        rtn = evalPython(evalstr).strip()
        repstr = "<?={}?>".format(match)
        str = str_replace(repstr,rtn,str)
    return str

def setView(name,clear=0):
    global VIEW
    if name in VIEWS:
        if clear == 1:
            VIEW = {}
        VIEW[name]=VIEWS[name]

def createView(name,val):
    global VIEW
    VIEW[name] = val
        
def removeView(name):
    global VIEW
    if name in VIEW:
        del VIEW[name]

def printValue(obj):
    print(pprint.pformat(obj).strip("'"))

def stringContains(str,substr):
    if substr in str:
        return True
    else:
        return False

def str_replace(str, str2, str3):
    result = str3.replace(str,str2)
    return result

def time():
    return ttime.time()






