#! python
"""
Installation
    python -m pip install sqlite3
References
    https://www.sqlitetutorial.net/sqlite-python/create-tables/
"""

#imports
try:
    import sqlite3
    from sqlite3 import Error
    import config
    import common
except ImportError as err:
    sys.exit(err)
###########################################
#Python’s default arguments are evaluated once when the function is defined, not each time the function is called.
def connect(params):
    try:
        dbconfig = {}
        #check config.CONFIG
        if 'dbname' in config.CONFIG:
            dbconfig['database'] = config.CONFIG['dbname']

        #check params and override any that are passed in
        if 'dbname' in params:
            dbconfig['database'] = params['dbname']

        # Connect
        conn_sqlite = sqlite.connect(dbconfig['database'])
        cur_sqlite = conn_sqlite.cursor(dictionary=True)
            
        #need to return both cur and conn so conn stays around
        return cur_sqlite, conn_sqlite
        
    except sqlite.Error as err:
        print("sqlitedb.connect error: {}".format(err))
        return false

###########################################
def queryResults(query,params):
    try:
        #connect
        cur_sqlite, conn_sqlite =  connect(params)
        #now execute the query
        cur_sqlite.execute(query)
        #NOTE: columns names can be accessed by cur_sqlite.column_names
        recs = cur_sqlite.fetchall()
        #NOTE: get row count with cur_sqlite.rowcount
        if type(recs) in (tuple, list):
            return recs
        else:
            return []
        
    except sqlite.Error as err:
        return ("sqlitedb.queryResults error: {}".format(err))
###########################################
