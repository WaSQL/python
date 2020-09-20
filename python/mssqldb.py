#! python
"""
Installation
    python -m pip install pymssql
References
    https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-3-proof-of-concept-connecting-to-sql-using-pymssql?view=sql-server-ver15
    https://pythonhosted.org/pymssql/pymssql_examples.html


"""


#imports
try:
    import pymssql
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
        if 'dbhost' in config.CONFIG:
            dbconfig['server'] = config.CONFIG['dbhost']

        if 'dbuser' in config.CONFIG:
            dbconfig['user'] = config.CONFIG['dbuser']

        if 'dbpass' in config.CONFIG:
            dbconfig['password'] = config.CONFIG['dbpass']

        if 'dbname' in config.CONFIG:
            dbconfig['database'] = config.CONFIG['dbname']

        #check params and override any that are passed in
        if 'dbhost' in params:
            dbconfig['server'] = params['dbhost']

        if 'dbuser' in params:
            dbconfig['user'] = params['dbuser']

        if 'dbpass' in params:
            dbconfig['password'] = params['dbpass']

        if 'dbname' in params:
            dbconfig['database'] = params['dbname']

        # Connect
        conn_pymssql = pymssql.connect(**dbconfig)
        cur_pymssql = conn_pymssql.cursor(dictionary=True)
            
        #need to return both cur and conn so conn stays around
        return cur_pymssql, conn_pymssql
        
    except pymssql.Error as err:
        print("pymssqldb.connect error: {}".format(err))
        return false

###########################################
def queryResults(query,params):
    try:
        #connect
        cur_pymssql, conn_pymssql =  connect(params)
        #now execute the query
        cur_pymssql.execute(query)
        #NOTE: columns names can be accessed by cur_pymssql.column_names
        recs = cur_pymssql.fetchall()
        #NOTE: get row count with cur_pymssql.rowcount
        if type(recs) in (tuple, list):
            return recs
        else:
            return []
        
    except pymssql.Error as err:
        return ("pymssqldb.queryResults error: {}".format(err))
###########################################
