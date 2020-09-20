#! python
"""
Installation
    python -m pip install cx_Oracle
References
    https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html#connpool
    https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html
"""


#imports
try:
    import cx_Oracle
    from cx_Oracle import Error
    from cx_Oracle import pooling
    import config
    import common
except ImportError as err:
    sys.exit(err)
###########################################
#Python’s default arguments are evaluated once when the function is defined, not each time the function is called.
def connect(params):
    try:
        dbconfig = {
            'min':2,
            'max':10,
            'increment':1,
            'encoding':'UTF-8'
        }
        #check config.CONFIG
        if 'dbhost' in config.CONFIG:
            dbconfig['host'] = config.CONFIG['dbhost']

        if 'dbuser' in config.CONFIG:
            dbconfig['user'] = config.CONFIG['dbuser']

        if 'dbpass' in config.CONFIG:
            dbconfig['password'] = config.CONFIG['dbpass']

        if 'dbname' in config.CONFIG:
            dbconfig['database'] = config.CONFIG['dbname']
        #check params and override any that are passed in
        if 'dbhost' in params:
            dbconfig['host'] = params['dbhost']

        if 'dbuser' in params:
            dbconfig['user'] = params['dbuser']

        if 'dbpass' in params:
            dbconfig['password'] = params['dbpass']

        if 'dbname' in params:
            dbconfig['database'] = params['dbname']
        #setup the connection pool
        pool_oracle = cx_Oracle.SessionPool(**dbconfig)

        # Get connection object from a pool if possible, otherwise just connect
        conn_oracle = pool_oracle.acquire()
        if conn_oracle.is_connected():
            cur_oracle = conn_oracle.cursor(dictionary=True)
        else:
            conn_oracle = cx_Oracle.connect(**dbconfig)
            cur_oracle = conn_oracle.cursor(dictionary=True)
        #need to return both cur and conn so conn stays around
        return cur_oracle, conn_oracle
        
    except cx_Oracle.Error as err:
        print("oracledb.connect error: {}".format(err))
        return false

###########################################
def queryResults(query,params):
    try:
        #connect
        cur_oracle, conn_oracle =  connect(params)
        #now execute the query
        cur_oracle.execute(query)
        #NOTE: columns names can be accessed by cur_oracle.column_names
        recs = cur_oracle.fetchall()
        #NOTE: get row count with cur_oracle.rowcount
        if type(recs) in (tuple, list):
            return recs
        else:
            return []
        
    except cx_Oracle.Error as err:
        return ("oracledb.queryResults error: {}".format(err))
###########################################
