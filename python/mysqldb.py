#! python
"""
Installation
    python -m pip install mysql.connector-python
       If it errors try these first
           python -m pip install -U setuptools
           python -m pip install -U wheel
References
    https://dev.mysql.com/doc/connector-python/en/connector-python-cext-reference.html
"""


#imports
try:
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import pooling
    import config
    import common
except ImportError as err:
    sys.exit(err)
###########################################
#Python’s default arguments are evaluated once when the function is defined, not each time the function is called.
def connect(params):
    try:
        dbconfig = {
            'pool_name':'wasql_pool',
            'pool_size':10,
            'pool_reset_session':True,
            'auth_plugin':'mysql_native_password'
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
        pool_mysql = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

        # Get connection object from a pool if possible, otherwise just connect
        conn_mysql = pool_mysql.get_connection()
        if conn_mysql.is_connected():
            cur_mysql = conn_mysql.cursor(dictionary=True)
        else:
            conn_mysql = mysql.connector.connect(**dbconfig)
            cur_mysql = conn_mysql.cursor(dictionary=True)
        #need to return both cur and conn so conn stays around
        return cur_mysql, conn_mysql
        
    except mysql.connector.Error as err:
        print("mysqldb.connect error: {}".format(err))
        return false

###########################################
def queryResults(query,params):
    try:
        #connect
        cur_mysql, conn_mysql =  connect(params)
        #now execute the query
        cur_mysql.execute(query)
        #NOTE: columns names can be accessed by cur_mysql.column_names
        recs = cur_mysql.fetchall()
        #NOTE: get row count with cur_mysql.rowcount
        if type(recs) in (tuple, list):
            return recs
        else:
            return []
        
    except mysql.connector.Error as err:
        return ("mysqldb.queryResults error: {}".format(err))
###########################################
